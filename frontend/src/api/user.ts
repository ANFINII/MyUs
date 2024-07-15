import { HttpStatusCode } from 'axios'
import { apiServer } from 'lib/apiServer'
import { apiClient, apiFormClient } from 'lib/axios'
import { Req } from 'types/global/next'
import { ProfileIn, ProfileOut, MypageIn, MypageOut, Follow, SearchTagOut, NotificationOut, NotificationIn } from 'types/internal/auth'
import { camelSnake } from 'utils/functions/convertCase'
import { apiProfile, apiMypage, apiFollow, apiFollower, apiSearchTag, apiNotification } from './uri'

export const getServerProfile = async (req: Req) => {
  const data = await apiServer(req, apiClient, apiProfile).then((res) => {
    if (res.status !== HttpStatusCode.Ok) return {}
    return res.data as ProfileOut
  })
  return data
}

export const getProfile = async (): Promise<ProfileOut> => {
  const data = await apiClient.get(apiProfile).then((res) => {
    return res.data as ProfileOut
  })
  return data
}

export const postProfile = async (request: ProfileIn) => {
  const data = await apiFormClient.post(apiProfile, camelSnake(request)).then((res) => {
    if (res.status !== HttpStatusCode.NoContent) {
      return res.data
    }
  })
  return data
}

export const getServerMypage = async (req: Req) => {
  const data = await apiServer(req, apiClient, apiMypage).then((res) => {
    if (res.status !== HttpStatusCode.Ok) return {}
    return res.data as MypageOut
  })
  return data
}

export const postMypage = async (request: MypageIn) => {
  const data = await apiFormClient.post(apiMypage, camelSnake(request)).then((res) => {
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
