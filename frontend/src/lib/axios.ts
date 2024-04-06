import axios, { AxiosInstance, AxiosResponse, AxiosError } from 'axios'
import { API_URL } from 'lib/config'
import { snakeCamel } from 'utils/functions/convertCase'

const responseInterceptor = (client: AxiosInstance) => {
  client.interceptors.response.use(
    (response: AxiosResponse) => {
      response.data = snakeCamel(response.data)
      return response
    },
    (e: AxiosError) => {
      const error = e.response
      console.log('===== error:', error, '=====')
      return Promise.resolve(error)
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
  responseInterceptor(client)
  return client
}

const axiosAddressInstance = (contentType: string) => {
  const client: AxiosInstance = axios.create({
    baseURL: 'https://zipcloud.ibsnet.co.jp',
    headers: { 'Content-Type': contentType },
    timeout: 5000,
  })
  responseInterceptor(client)
  return client
}

export const apiClient = axiosInstance('application/json')
export const apiFormClient = axiosInstance('multipart/form-data')
export const apiAddressClient = axiosAddressInstance('application/json')
