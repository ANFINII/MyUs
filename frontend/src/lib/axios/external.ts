import axios, { AxiosInstance } from 'axios'
import { axiosInterceptor } from '.'

const axiosInstance = (baseURL: string) => {
  const client: AxiosInstance = axios.create({
    baseURL,
    headers: { 'Content-Type': 'application/json' },
    timeout: 5000,
  })
  axiosInterceptor(client)
  return client
}

export const apiAddressClient = axiosInstance('https://zipcloud.ibsnet.co.jp')
