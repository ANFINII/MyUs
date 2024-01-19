import { NextApiRequestCookies } from 'next/dist/server/api-utils'
import { IncomingMessage } from 'http'
import { apiServer } from 'lib/apiServer'
import { apiClient } from 'lib/axios'
import { UserProfile, Mypage } from 'types/internal/auth'
import { Notification } from 'types/internal/auth'
import { apiProfile, apiMypage, apiNotification } from './uri'

interface Req extends IncomingMessage {
  cookies: NextApiRequestCookies
}

export const getProfile = async (req: Req) => {
  const data = await apiServer(req, apiClient, apiProfile).then((res) => {
    return res.data as UserProfile
  })
  return data
}

export const getMypage = async (req: Req) => {
  const data = await apiServer(req, apiClient, apiMypage).then((res) => {
    return res.data as Mypage
  })
  return data
}

export const getNotification = async (req: Req) => {
  const data = await apiServer(req, apiClient, apiNotification).then((res) => {
    return res.data as Notification
  })
  return data
}
