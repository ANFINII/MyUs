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
      console.log('===== error status:', error?.status, error?.statusText, '=====')

      const message = error?.data?.error
      if (message) {
        console.log('===== error message:', message, '=====')
      }

      if (error?.status >= 400) {
        return Promise.resolve({ data: {} })
      }

      return Promise.reject(error)
    },
  )
}

const createAxiosInstance = (contentType: string) => {
  const client: AxiosInstance = axios.create({
    baseURL: API_URL,
    withCredentials: true,
    headers: {
      'Content-Type': contentType,
    },
    timeout: 1000,
  })
  applyResponseInterceptor(client)
  return client
}

export const apiClient = createAxiosInstance('application/json')
