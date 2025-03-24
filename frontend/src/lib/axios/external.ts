import axios, { AxiosInstance, AxiosResponse, AxiosError } from 'axios'
import { AxiosErrorLog } from 'lib/config'
import { snakeCamel } from 'utils/functions/convertCase'

const responseInterceptor = (client: AxiosInstance) => {
  client.interceptors.response.use(
    (response: AxiosResponse) => {
      response.data = snakeCamel(response.data)
      return response
    },
    (e: AxiosError) => {
      AxiosErrorLog(e)
      return Promise.resolve(e.response)
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
