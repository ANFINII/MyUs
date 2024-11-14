import { HttpStatusCode } from 'axios'
import { apiClient } from 'lib/axios'
import { cookieHeader } from 'lib/config'
import { Req } from 'types/global'
import { MediaHome, Video, Music, Comic, Picture, Blog, Chat, Todo } from 'types/internal/media'
import { apiHome, apiVideos, apiMusics, apiComics, apiPictures, apiBlogs, apiChats, apiTodos } from 'api/uri'

export const getHome = async (search?: string, req?: Req): Promise<MediaHome> => {
  const res = await apiClient.get(apiHome, cookieHeader(req, { search }))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getVideos = async (search?: string, req?: Req): Promise<Video[]> => {
  const res = await apiClient.get(apiVideos, cookieHeader(req, { search }))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getMusics = async (search?: string, req?: Req): Promise<Music[]> => {
  const res = await apiClient.get(apiMusics, cookieHeader(req, { search }))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getComics = async (search?: string, req?: Req): Promise<Comic[]> => {
  const res = await apiClient.get(apiComics, cookieHeader(req, { search }))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getPictures = async (search?: string, req?: Req): Promise<Picture[]> => {
  const res = await apiClient.get(apiPictures, cookieHeader(req, { search }))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getBlogs = async (search?: string, req?: Req): Promise<Blog[]> => {
  const res = await apiClient.get(apiBlogs, cookieHeader(req, { search }))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getChats = async (search?: string, req?: Req): Promise<Chat[]> => {
  const res = await apiClient.get(apiChats, cookieHeader(req, { search }))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getTodos = async (search?: string, req?: Req): Promise<Todo[]> => {
  const res = await apiClient.get(apiTodos, cookieHeader(req, { search }))
  if (res.status >= HttpStatusCode.BadRequest) return []
  return res.data
}
