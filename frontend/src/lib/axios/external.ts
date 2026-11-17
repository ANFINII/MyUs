import axios from 'axios'
import { axiosInterceptor } from '.'

const axiosInstance = (baseURL: string, contentType: string) => {
  const client = axios.create({
    baseURL,
    headers: { 'Content-Type': contentType },
    timeout: 5000,
  })
  axiosInterceptor(client)
  return client
}

export const apiAddressClient = axiosInstance('https://zipcloud.ibsnet.co.jp', 'application/json')
