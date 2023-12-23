import { IncomingMessage } from 'http'
import { AxiosInstance } from 'axios'

export const apiServer = async (req: IncomingMessage, client: AxiosInstance, url: string, query?: any, header?: Record<string, string>) => {
  const cookie = req.headers.cookie
  const headers = { cookie, ...(header && { ...header }) }
  const config = { headers, ...(query && { params: query }) }
  return await client.get(url, config)
}
