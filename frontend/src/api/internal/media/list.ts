import { HttpStatusCode } from 'axios'
import { apiClient } from 'lib/axios/internal'
import { cookieHeader } from 'lib/config'
import { Req } from 'types/global'
import { SearchParms, MediaHome, Video, Music, Comic, Picture, Blog, Chat } from 'types/internal/media'
import { apiHome, apiVideos, apiMusics, apiComics, apiPictures, apiBlogs, apiChats } from 'api/uri'

export const getHome = async (params: SearchParms, req?: Req): Promise<MediaHome> => {
  const res = await apiClient.get(apiHome, cookieHeader(req, params))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getVideos = async (params: SearchParms, req?: Req): Promise<Video[]> => {
  const res = await apiClient.get(apiVideos, cookieHeader(req, params))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getMusics = async (params: SearchParms, req?: Req): Promise<Music[]> => {
  const res = await apiClient.get(apiMusics, cookieHeader(req, params))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getComics = async (params: SearchParms, req?: Req): Promise<Comic[]> => {
  const res = await apiClient.get(apiComics, cookieHeader(req, params))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getPictures = async (params: SearchParms, req?: Req): Promise<Picture[]> => {
  const res = await apiClient.get(apiPictures, cookieHeader(req, params))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getBlogs = async (params: SearchParms, req?: Req): Promise<Blog[]> => {
  const res = await apiClient.get(apiBlogs, cookieHeader(req, params))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getChats = async (params: SearchParms, req?: Req): Promise<Chat[]> => {
  const res = await apiClient.get(apiChats, cookieHeader(req, params))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}
