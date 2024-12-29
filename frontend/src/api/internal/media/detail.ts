import { HttpStatusCode } from 'axios'
import { apiClient } from 'lib/axios'
import { cookieHeader } from 'lib/config'
import { Req } from 'types/global'
import { Video, Music, Comic, Picture, Chat, Todo, BlogDetailOut, CommnetIn } from 'types/internal/media'
import { apiVideo, apiMusic, apiComic, apiPicture, apiBlog, apiChat, apiTodo, apiCommnet } from 'api/uri'

export const getVideo = async (id: number, req?: Req): Promise<Video> => {
  const res = await apiClient.get(apiVideo(id), cookieHeader(req))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getMusic = async (id: number, req?: Req): Promise<Music> => {
  const res = await apiClient.get(apiMusic(id), cookieHeader(req))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getComic = async (id: number, req?: Req): Promise<Comic> => {
  const res = await apiClient.get(apiComic(id), cookieHeader(req))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getPicture = async (id: number, req?: Req): Promise<Picture> => {
  const res = await apiClient.get(apiPicture(id), cookieHeader(req))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getBlog = async (id: number, req?: Req): Promise<BlogDetailOut> => {
  const res = await apiClient.get(apiBlog(id), cookieHeader(req))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getChat = async (id: number, req?: Req): Promise<Chat> => {
  const res = await apiClient.get(apiChat(id), cookieHeader(req))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getTodo = async (id: number, req?: Req): Promise<Todo[]> => {
  const res = await apiClient.get(apiTodo(id), cookieHeader(req))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const createComment = async (id: number, request: CommnetIn): Promise<void> => {
  const res = await apiClient.post(apiCommnet(id), request)
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}
