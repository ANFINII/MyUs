import { AxiosInstance, AxiosResponse, AxiosError } from 'axios'
import { AxiosErrorLog } from 'lib/config'
import { snakeCamel } from 'utils/functions/convertCase'

export const axiosInterceptor = (client: AxiosInstance) => {
  client.interceptors.response.use(
    (response: AxiosResponse) => {
      response.data = snakeCamel(response.data)
      return response
    },
    (e: AxiosError) => {
      AxiosErrorLog(e)
      const status = e.response?.status
      if (status && (status === 422 || status >= 500)) {
        return Promise.reject(e.response)
      }
      return Promise.resolve(e.response)
    },
  )
}
