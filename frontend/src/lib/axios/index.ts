import { AxiosInstance, AxiosResponse, AxiosError } from 'axios'
import { snakeCamel } from 'utils/functions/convertCase'

export const axiosInterceptor = (client: AxiosInstance) => {
  client.interceptors.response.use(
    (response: AxiosResponse) => {
      response.data = snakeCamel(response.data)
      return response
    },
    (e: AxiosError) => {
      const status = e.response?.status
      if (status && status >= 400) {
        return Promise.reject(e)
      }
      return Promise.resolve(e.response)
    },
  )
}
