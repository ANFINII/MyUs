import axios, { AxiosError, AxiosInstance, AxiosResponse, InternalAxiosRequestConfig } from 'axios'
import { API_URL } from 'lib/config'
import { apiRefresh } from 'api/uri'
import { ErrorType } from 'utils/constants/enum'

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

export const retryWithRefresh = async (client: AxiosInstance, e: AxiosError): Promise<AxiosResponse | null> => {
  const config = e.config as RetryConfig | undefined
  if (config === undefined || config.isRetry || !isUnauthenticated(e)) return null

  const isRefreshed = await refreshToken()
  if (!isRefreshed) return null

  return client.request({ ...config, isRetry: true } as RetryConfig)
}
