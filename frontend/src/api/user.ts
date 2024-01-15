import { NextApiRequestCookies } from 'next/dist/server/api-utils'
import { IncomingMessage } from 'http'
import { HttpStatusCode } from 'axios'
import { apiServer } from 'lib/apiServer'
import { apiClient } from 'lib/axios'
import { apiProfile, apiMypage } from './uri'

interface Req extends IncomingMessage {
  cookies: NextApiRequestCookies
}

export const getProfile = async (req: Req) => {
  const data = await apiServer(req, apiClient, apiProfile).then((res) => {
    if (res.status !== HttpStatusCode.Ok) throw Error
    return res.data
  })
  return data
}

export const getMypage = async (req: Req) => {
  const data = await apiServer(req, apiClient, apiMypage).then((res) => {
    if (res.status !== HttpStatusCode.Ok) throw Error
    return res.data
  })
  return data
}
