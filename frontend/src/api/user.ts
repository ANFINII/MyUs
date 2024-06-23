import { HttpStatusCode } from 'axios'
import { apiServer } from 'lib/apiServer'
import { apiClient } from 'lib/axios'
import { Req } from 'types/global/next'
import { UserProfile, Mypage, MypageIn, Follow, SearchTagOut, NotificationOut, NotificationIn } from 'types/internal/auth'
import { camelSnake } from 'utils/functions/convertCase'
import { apiProfile, apiMypage, apiFollow, apiFollower, apiSearchTag, apiNotification } from './uri'

export const getServerProfile = async (req: Req) => {
  const data = await apiServer(req, apiClient, apiProfile).then((res) => {
    if (res.status !== HttpStatusCode.Ok) return {}
    return res.data as UserProfile
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
    if (res.status !== HttpStatusCode.Ok) return {}
    return res.data as Mypage
  })
  return data
}

export const postMypage = async (request: MypageIn) => {
  const data = await apiClient.post(apiMypage, camelSnake(request)).then((res) => {
    if (res.status !== HttpStatusCode.NoContent) {
      return res.data
    }
  })
  return data
}

export const getServerFollow = async (req: Req) => {
  const data = await apiServer(req, apiClient, apiFollow).then((res) => {
    if (res.status !== HttpStatusCode.Ok) return {}
    return res.data as Follow[]
  })
  return data
}

export const getServerFollower = async (req: Req) => {
  const data = await apiServer(req, apiClient, apiFollower).then((res) => {
    if (res.status !== HttpStatusCode.Ok) return {}
    return res.data as Follow[]
  })
  return data
}

export const getSearchTag = async () => {
  const data = await apiClient.get(apiSearchTag).then((res) => {
    return res.data as SearchTagOut[]
  })
  return data
}

export const getServerNotification = async (req: Req) => {
  const data = await apiServer(req, apiClient, apiNotification).then((res) => {
    if (res.status !== HttpStatusCode.Ok) return null
    return res.data as NotificationOut
  })
  return data
}

export const getNotification = async () => {
  const data = await apiClient.get(apiNotification).then((res) => {
    return res.data as NotificationOut
  })
  return data
}

export const postNotification = async (request: NotificationIn) => {
  await apiClient.post(apiNotification, camelSnake(request))
}
