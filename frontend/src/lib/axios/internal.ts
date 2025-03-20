import axios, { AxiosInstance, AxiosResponse, AxiosError } from 'axios'
import { API_URL, AxiosErrorLog } from 'lib/config'
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
  responseInterceptor(client)
  return client
}

export const apiClient = axiosInstance(API_URL, 'application/json')
export const apiFormClient = axiosInstance(API_URL, 'multipart/form-data')
