import axios, { AxiosInstance, AxiosResponse, AxiosError, InternalAxiosRequestConfig } from 'axios'
import { API_URL } from 'lib/config'
import { apiRefresh } from 'api/uri'
import { ErrorType } from 'utils/constants/enum'
import { snakeCamel } from 'utils/functions/convertCase'

interface RetryConfig extends InternalAxiosRequestConfig {
  isRetry?: boolean
}

let refreshPromise: Promise<boolean> | null = null

const refreshToken = (): Promise<boolean> => {
  if (refreshPromise === null) {
    refreshPromise = axios
      .post(API_URL + apiRefresh, null, { withCredentials: true })
      .then(() => true)
      .catch(() => false)
      .finally(() => {
        refreshPromise = null
      })
  }
  return refreshPromise
}

const isUnauthenticated = (e: AxiosError): boolean => {
  const data = e.response?.data as { type?: string } | undefined
  return e.response?.status === 400 && data?.type === ErrorType.Unauthenticated
}

export const axiosInterceptor = (client: AxiosInstance) => {
  client.interceptors.response.use(
    (response: AxiosResponse) => {
      response.data = snakeCamel(response.data)
      return response
    },
    async (e: AxiosError) => {
      const config = e.config as RetryConfig | undefined
      if (config !== undefined && !config.isRetry && isUnauthenticated(e)) {
        const isRefreshed = await refreshToken()
        if (isRefreshed) {
          return client.request({ ...config, isRetry: true } as RetryConfig)
        }
      }

      const status = e.response?.status
      if (status && status >= 400) {
        return Promise.reject(e)
      }
      return Promise.resolve(e.response)
    },
  )
}
