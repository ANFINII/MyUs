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
          console.log('401 Unauthorized')
          break
        case 404:
          console.log('404 Not Found')
          break
        default:
          console.log('Internal Server Error')
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
