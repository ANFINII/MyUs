import axios, { AxiosInstance, AxiosResponse } from 'axios'
import { API_URL } from 'lib/config'
import { snakeCamel } from 'utils/functins/convertCase'

const applyResponseInterceptor = (client: AxiosInstance) => {
  client.interceptors.response.use(
    (response: AxiosResponse) => {
      response.data = snakeCamel(response.data)
      return response
    },
    (error) => {
      console.log('error:', error)
      switch (error?.response?.status) {
        case 401:
          break
        case 404:
          break
        default:
          console.log('== internal server error')
      }
      const message = (error.response?.data?.message || '').split(',')
      console.log('error message:', message)
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
  })
  applyResponseInterceptor(client)
  return client
}

export const apiClient: AxiosInstance = createAxiosInstance('application/json')
