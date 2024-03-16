import { AxiosInstance, AxiosResponse } from 'axios'
import { Req } from 'types/global/next'

type Query = Record<string, string>

export const apiServer = async (req: Req, client: AxiosInstance, url: string, query?: Query, header?: Query): Promise<AxiosResponse> => {
  const cookie = req.headers.cookie
  const headers = { cookie, ...(header && { ...header }) }
  const config = { headers, ...(query && { params: query }) }
  return await client.get(url, config)
}
