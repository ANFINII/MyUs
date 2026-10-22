import { AxiosInstance, AxiosResponse, AxiosError } from 'axios'
import { snakeCamel } from 'utils/functions/convertCase'
import { retryWithRefresh } from './refresh'

export const axiosInterceptor = (client: AxiosInstance) => {
  client.interceptors.response.use(
    (response: AxiosResponse) => {
      response.data = snakeCamel(response.data)
      return response
    },
    (e: AxiosError) => {
      return retryWithRefresh(client, e).then((retried) => {
        if (retried !== null) return retried
        return Promise.reject(e)
      })
    },
  )
}
