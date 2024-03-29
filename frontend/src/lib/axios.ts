import axios, { AxiosInstance, AxiosResponse } from 'axios'
import { API_URL } from 'lib/config'
import { snakeCamel } from 'utils/functions/convertCase'

const applyResponseInterceptor = (client: AxiosInstance) => {
  client.interceptors.response.use(
    (response: AxiosResponse) => {
      response.data = snakeCamel(response.data)
      return response
    },
    (e) => {
      const error = e.response
      const message = error?.data?.message
      const response = message ? { data: { message } } : { data: {} }

      console.log('===== error status:', error?.status, error?.statusText, '=====')
      if (message) {
        console.log('===== error message:', message, '=====')
      }

      if (error?.status >= 400) {
        return Promise.resolve(response)
      }
    },
  )
}

const axiosInstance = (contentType: string, csrfToken?: string) => {
  const client: AxiosInstance = axios.create({
    baseURL: API_URL,
    withCredentials: true,
    headers: {
      'Content-Type': contentType,
      'X-CSRFToken': csrfToken,
    },
    timeout: 2000,
    paramsSerializer: { indexes: null },
  })
  applyResponseInterceptor(client)
  return client
}

const axiosAddressInstance = (contentType: string) => {
  const client: AxiosInstance = axios.create({
    baseURL: 'https://zipcloud.ibsnet.co.jp',
    headers: { 'Content-Type': contentType },
    timeout: 5000,
  })
  applyResponseInterceptor(client)
  return client
}

export const apiClient = axiosInstance('application/json')
export const apiFormClient = axiosInstance('multipart/form-data')
export const apiAddressClient = axiosAddressInstance('application/json')
