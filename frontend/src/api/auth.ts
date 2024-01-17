import { NextApiRequestCookies } from 'next/dist/server/api-utils'
import { IncomingMessage } from 'http'
import { HttpStatusCode } from 'axios'
import { apiServer } from 'lib/apiServer'
import { apiClient } from 'lib/axios'
import { apiAuth } from './uri'

interface Req extends IncomingMessage {
  cookies: NextApiRequestCookies
}

export const getAuth = async (req: Req) => {
  const data = await apiServer(req, apiClient, apiAuth).then((res) => {
    return res.status === HttpStatusCode.Ok
  })
  return data
}
