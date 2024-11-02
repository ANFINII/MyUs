import { HttpStatusCode } from 'axios'
import { apiClient } from 'lib/axios'
import { cookieHeader } from 'lib/config'
import { Req } from 'types/global'
import { MediaHome, Video, Music, Comic, Picture, Blog, Chat, Todo } from 'types/internal/media'
import { apiHome, apiVideos, apiMusics, apiComics, apiPictures, apiBlogs, apiChats, apiTodos } from 'api/uri'

export const getHome = async (search?: string): Promise<MediaHome> => {
  const res = await apiClient.get(apiHome, { params: { search } })
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getVideos = async (search?: string): Promise<Video[]> => {
  const res = await apiClient.get(apiVideos, { params: { search } })
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getMusics = async (search?: string): Promise<Music[]> => {
  const res = await apiClient.get(apiMusics, { params: { search } })
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getComics = async (search?: string): Promise<Comic[]> => {
  const res = await apiClient.get(apiComics, { params: { search } })
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getPictures = async (search?: string): Promise<Picture[]> => {
  const res = await apiClient.get(apiPictures, { params: { search } })
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getBlogs = async (search?: string): Promise<Blog[]> => {
  const res = await apiClient.get(apiBlogs, { params: { search } })
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getChats = async (search?: string): Promise<Chat[]> => {
  const res = await apiClient.get(apiChats, { params: { search } })
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getTodos = async (req?: Req, search?: string): Promise<Todo[]> => {
  const res = await apiClient.get(apiTodos, cookieHeader(req, { search }))
  if (res.status >= HttpStatusCode.BadRequest) return []
  return res.data
}
