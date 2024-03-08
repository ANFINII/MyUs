import { AxiosInstance, AxiosResponse } from 'axios'
import { Req } from 'types/global/next'

export const apiServer = async (
  req: Req,
  client: AxiosInstance,
  url: string,
  query?: Record<string, string>,
  header?: Record<string, string>,
): Promise<AxiosResponse> => {
  const cookie = req.headers.cookie
  const headers = { cookie, ...(header && { ...header }) }
  const config = { headers, ...(query && { params: query }) }
  return await client.get(url, config)
}
