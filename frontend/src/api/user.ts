import { HttpStatusCode } from 'axios'
import { apiServer } from 'lib/apiServer'
import { apiClient, apiFormClient } from 'lib/axios'
import { Req } from 'types/global/next'
import { ProfileIn, ProfileOut, MypageIn, MypageOut, Follow, SearchTagOut, NotificationOut, NotificationIn } from 'types/internal/auth'
import { MessageOut } from 'types/internal/other'
import { camelSnake } from 'utils/functions/convertCase'
import { apiProfile, apiMypage, apiFollow, apiFollower, apiSearchTag, apiNotification } from './uri'

export const getServerProfile = async (req: Req): Promise<ProfileOut> => {
  const data = await apiServer(req, apiClient, apiProfile).then((res) => {
    if (res.status !== HttpStatusCode.Ok) return {}
    return res.data
  })
  return data
}

export const getProfile = async (): Promise<ProfileOut> => {
  const data = await apiClient.get(apiProfile).then((res) => {
    return res.data
  })
  return data
}

export const putProfile = async (request: ProfileIn): Promise<MessageOut | void> => {
  const data = await apiFormClient.put(apiProfile, camelSnake(request)).then((res) => {
    if (res.status === HttpStatusCode.InternalServerError) throw Error
    return res.data
  })
  return data
}

export const getServerMypage = async (req: Req): Promise<MypageOut> => {
  const data = await apiServer(req, apiClient, apiMypage).then((res) => {
    if (res.status !== HttpStatusCode.Ok) return {}
    return res.data
  })
  return data
}

export const putMypage = async (request: MypageIn): Promise<MessageOut | void> => {
  const data = await apiFormClient.put(apiMypage, camelSnake(request)).then((res) => {
    if (res.status === HttpStatusCode.InternalServerError) throw Error
    return res.data
  })
  return data
}

export const getServerFollow = async (req: Req): Promise<Follow[]> => {
  const data = await apiServer(req, apiClient, apiFollow).then((res) => {
    if (res.status !== HttpStatusCode.Ok) return []
    return res.data
  })
  return data
}

export const getServerFollower = async (req: Req): Promise<Follow[]> => {
  const data = await apiServer(req, apiClient, apiFollower).then((res) => {
    if (res.status !== HttpStatusCode.Ok) return []
    return res.data
  })
  return data
}

export const getSearchTag = async (): Promise<SearchTagOut[]> => {
  const data = await apiClient.get(apiSearchTag).then((res) => {
    return res.data
  })
  return data
}

export const getServerNotification = async (req: Req): Promise<NotificationOut> => {
  const data = await apiServer(req, apiClient, apiNotification).then((res) => {
    return res.data
  })
  return data
}

export const getNotification = async (): Promise<NotificationOut> => {
  const data = await apiClient.get(apiNotification).then((res) => {
    return res.data as NotificationOut
  })
  return data
}

export const postNotification = async (request: NotificationIn): Promise<void> => {
  await apiClient.post(apiNotification, camelSnake(request))
}
