import { NextApiRequestCookies } from 'next/dist/server/api-utils'
import { IncomingMessage } from 'http'

export type Header = Record<string, string>

export type CookieHeaders = {
  cookie?: string
}

export interface Req extends IncomingMessage {
  cookies: NextApiRequestCookies
}

export interface Config {
  params?: Query | undefined
  headers: CookieHeaders
}
