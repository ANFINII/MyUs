import { HttpStatusCode } from 'axios'
import { apiServer } from 'lib/apiServer'
import { apiClient } from 'lib/axios'
import { Req } from 'types/global/next'
import { Follow, SearchTagOut } from 'types/internal/auth'
import { apiFollow, apiFollower, apiSearchTag } from '../uri'

export const getSearchTag = async (): Promise<SearchTagOut[]> => {
  const res = await apiClient.get(apiSearchTag)
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getServerFollow = async (req: Req): Promise<Follow[]> => {
  const res = await apiServer(req, apiClient, apiFollow)
  if (res.status >= HttpStatusCode.BadRequest) return []
  return res.data
}

export const getFollow = async (search?: string): Promise<Follow[]> => {
  const res = await apiClient.get(apiFollow, { params: { search } })
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getServerFollower = async (req: Req): Promise<Follow[]> => {
  const res = await apiServer(req, apiClient, apiFollower)
  if (res.status >= HttpStatusCode.BadRequest) return []
  return res.data
}

export const getFollower = async (search?: string): Promise<Follow[]> => {
  const res = await apiClient.get(apiFollower, { params: { search } })
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}
