import axios, { AxiosInstance } from 'axios'
import { API_URL } from 'lib/config'
import { axiosInterceptor } from '.'

type ContentType = 'json' | 'form'

const JSON_TIMEOUT_MS = 10000 // 10秒
const FILE_UPLOAD_TIMEOUT_MS = 60000 // 1分

const axiosInstance = (baseURL: string, contentType: ContentType) => {
  const client: AxiosInstance = axios.create({
    baseURL,
    withCredentials: true,
    headers: {
      'Content-Type': contentType === 'json' ? 'application/json' : 'multipart/form-data',
    },
    timeout: contentType === 'json' ? JSON_TIMEOUT_MS : FILE_UPLOAD_TIMEOUT_MS,
    paramsSerializer: { indexes: null },
    formSerializer: { indexes: null },
  })
  axiosInterceptor(client)
  return client
}

export const apiClient = (type: ContentType) => axiosInstance(API_URL, type)
