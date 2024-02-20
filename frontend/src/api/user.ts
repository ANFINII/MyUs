import { HttpStatusCode } from 'axios'
import { apiServer } from 'lib/apiServer'
import { apiClient } from 'lib/axios'
import { Req } from 'types/global/next'
import { UserProfile, Mypage } from 'types/internal/auth'
import { Notification } from 'types/internal/auth'
import { camelSnake } from 'utils/functions/convertCase'
import { apiProfile, apiMypage, apiNotification } from './uri'

export const getProfile = async (req: Req) => {
  const data = await apiServer(req, apiClient, apiProfile).then((res) => {
    if (res.status === HttpStatusCode.Ok) {
      return res.data as UserProfile
    } else {
      return {}
    }
  })
  return data
}

export const postProfile = async (request: UserProfile) => {
  const data = await apiClient.post(apiProfile, camelSnake(request)).then((res) => {
    if (res.status !== HttpStatusCode.NoContent) {
      return res.data
    }
  })
  return data
}

export const getServerMypage = async (req: Req) => {
  const data = await apiServer(req, apiClient, apiMypage).then((res) => {
    if (res.status === HttpStatusCode.Ok) {
      return res.data as Mypage
    } else {
      return {}
    }
  })
  return data
}

export const getServerNotification = async (req: Req) => {
  const data = await apiServer(req, apiClient, apiNotification).then((res) => {
    if (res.status === HttpStatusCode.Ok) {
      return res.data as Notification
    } else {
      return {}
    }
  })
  return data
}
