import { apiServer } from 'lib/apiServer'
import { apiClient } from 'lib/axios'
import { Req } from 'types/global/next'
import { UserProfile, Mypage } from 'types/internal/auth'
import { Notification } from 'types/internal/auth'
import { apiProfile, apiMypage, apiNotification } from './uri'

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
