import axios, { AxiosInstance } from 'axios'
import { API_URL } from 'lib/config'
import { axiosInterceptor } from '.'

const axiosInstance = (baseURL: string, contentType: string, csrfToken?: string) => {
  const client: AxiosInstance = axios.create({
    baseURL,
    withCredentials: true,
    headers: {
      'Content-Type': contentType,
      'X-CSRFToken': csrfToken,
    },
    timeout: 2000,
    paramsSerializer: { indexes: null },
  })
  axiosInterceptor(client)
  return client
}

export const apiClient = axiosInstance(API_URL, 'application/json')
export const apiFormClient = axiosInstance(API_URL, 'multipart/form-data')
