import { HttpStatusCode } from 'axios'
import { apiClient } from 'lib/axios'
import { apiVideo, apiMusic, apiComic, apiPicture, apiBlog, apiChat, apiTodo } from 'api/uri'
import { Video, Music, Comic, Picture, Blog, Chat, Todo } from 'types/internal/media'

export const getVideo = async (id: number): Promise<Video> => {
  const res = await apiClient.get(apiVideo(id))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getMusic = async (id: number): Promise<Music> => {
  const res = await apiClient.get(apiMusic(id))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getComic = async (id: number): Promise<Comic> => {
  const res = await apiClient.get(apiComic(id))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getPicture = async (id: number): Promise<Picture> => {
  const res = await apiClient.get(apiPicture(id))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getBlog = async (id: number): Promise<Blog> => {
  const res = await apiClient.get(apiBlog(id))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getChat = async (id: number): Promise<Chat> => {
  const res = await apiClient.get(apiChat(id))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}

export const getToDo = async (id: number): Promise<Todo> => {
  const res = await apiClient.get(apiTodo(id))
  if (res.status >= HttpStatusCode.InternalServerError) throw Error
  return res.data
}
