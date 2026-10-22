import { AxiosInstance, AxiosResponse, AxiosError } from 'axios'
import { snakeCamel } from 'utils/functions/convertCase'
import { retryWithRefresh } from './refresh'

export const axiosInterceptor = (client: AxiosInstance) => {
  client.interceptors.response.use(
    (response: AxiosResponse) => {
      response.data = snakeCamel(response.data)
      return response
    },
    async (e: AxiosError) => {
      const retried = await retryWithRefresh(client, e)
      if (retried !== null) return retried

      const status = e.response?.status
      if (status && status >= 400) {
        return Promise.reject(e)
      }
      return Promise.resolve(e.response)
    },
  )
}
