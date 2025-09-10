import axios, { AxiosInstance } from 'axios'
import { API_URL } from 'lib/config'
import { axiosInterceptor } from '.'

const FILE_UPLOAD_TIMEOUT_MS = 60000 // 1分

const axiosInstance = (baseURL: string, contentType: string, timeout?: number) => {
  const client: AxiosInstance = axios.create({
    baseURL,
    withCredentials: true,
    headers: {
      'Content-Type': contentType,
    },
    timeout: timeout || 2000,
    paramsSerializer: { indexes: null },
  })
  axiosInterceptor(client)
  return client
}

export const apiClient = axiosInstance(API_URL, 'application/json')
export const apiFormClient = axiosInstance(API_URL, 'multipart/form-data', FILE_UPLOAD_TIMEOUT_MS)
