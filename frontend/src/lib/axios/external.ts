import axios, { AxiosInstance, AxiosResponse, AxiosError } from 'axios'
import { snakeCamel } from 'utils/functions/convertCase'

const responseInterceptor = (client: AxiosInstance) => {
  client.interceptors.response.use(
    (response: AxiosResponse) => {
      return snakeCamel(response.data)
    },
    (e: AxiosError) => {
      const error = e.response
      console.log('===== error:', error, '=====')
      return Promise.resolve(error)
    },
  )
}

const axiosInstance = (baseURL: string) => {
  const client: AxiosInstance = axios.create({
    baseURL,
    headers: { 'Content-Type': 'application/json' },
    timeout: 5000,
  })
  responseInterceptor(client)
  return client
}

export const apiAddressClient = axiosInstance('https://zipcloud.ibsnet.co.jp')
