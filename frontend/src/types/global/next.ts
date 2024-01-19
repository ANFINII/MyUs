import { NextApiRequestCookies } from 'next/dist/server/api-utils'
import { IncomingMessage } from 'http'

export interface Req extends IncomingMessage {
  cookies: NextApiRequestCookies
}
