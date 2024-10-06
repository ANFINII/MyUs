import { HttpStatusCode } from 'axios'
import { apiServer } from 'lib/apiServer'
import { apiClient } from 'lib/axios'
import { apiVideo, apiMusic, apiComic, apiPicture, apiBlog, apiChat, apiTodo } from 'api/uri'
import { Req } from 'types/global/next'
import { Video, Music, Comic, Picture, Chat, Todo, BlogDetailOut } from 'types/internal/media'

export const getServerVideo = async (req: Req, id: number): Promise<Video> => {
  const res = await apiServer(req, apiClient, apiVideo(id))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getServerMusic = async (req: Req, id: number): Promise<Music> => {
  const res = await apiServer(req, apiClient, apiMusic(id))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getServerComic = async (req: Req, id: number): Promise<Comic> => {
  const res = await apiServer(req, apiClient, apiComic(id))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getServerPicture = async (req: Req, id: number): Promise<Picture> => {
  const res = await apiServer(req, apiClient, apiPicture(id))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getServerBlog = async (req: Req, id: number): Promise<BlogDetailOut> => {
  const res = await apiServer(req, apiClient, apiBlog(id))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getServerChat = async (req: Req, id: number): Promise<Chat> => {
  const res = await apiServer(req, apiClient, apiChat(id))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getServerTodo = async (req: Req, id: number): Promise<Todo[]> => {
  const res = await apiServer(req, apiClient, apiTodo(id))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}
