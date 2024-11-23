import { NextApiRequestCookies } from 'next/dist/server/api-utils'
import { IncomingMessage } from 'http'

export type Query = Record<string, string | undefined>
export type Header = Record<string, string>

export interface Req extends IncomingMessage {
  cookies: NextApiRequestCookies
}

export const CookieHeaders: {
  cookie: NextApiRequestCookies
}

export interface Config {
  params?: Query | undefined
  headers: CookieHeaders
}
