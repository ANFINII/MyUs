import { NextApiRequestCookies } from 'next/dist/server/api-utils'
import { IncomingMessage } from 'http'

export type Query = Record<string, string | undefined>
export type Header = Record<string, string>
export type Cookie = string | undefined

export type CookieHeaders = {
  cookie: Cookie
}

export interface Req extends IncomingMessage {
  cookies: NextApiRequestCookies
}

export interface Config {
  params?: Query | undefined
  headers: CookieHeaders
}
