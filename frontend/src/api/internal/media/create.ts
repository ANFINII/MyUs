import { HttpStatusCode } from 'axios'
import { apiFormClient, apiClient } from 'lib/axios/internal'
import { Video, Music, Comic, Picture, Blog, Chat, Todo, TodoIn } from 'types/internal/media'
import { VideoIn, MusicIn, ComicIn, PictureIn, BlogIn, ChatIn } from 'types/internal/media'
import { apiVideoCreate, apiMusicCreate, apiComicCreate, apiPictureCreate, apiBlogCreate, apiChatCreate, apiTodoCreate } from 'api/uri'

export const postVideoCreate = async (request: VideoIn): Promise<Video> => {
  const res = await apiFormClient.post(apiVideoCreate, request)
  if (res.status >= HttpStatusCode.BadRequest) throw Error
  return res.data
}

export const postMusicCreate = async (request: MusicIn): Promise<Music> => {
  const res = await apiFormClient.post(apiMusicCreate, request)
  if (res.status >= HttpStatusCode.BadRequest) throw Error
  return res.data
}

export const postComicCreate = async (request: ComicIn): Promise<Comic> => {
  const res = await apiFormClient.post(apiComicCreate, request)
  if (res.status >= HttpStatusCode.BadRequest) throw Error
  return res.data
}

export const postPictureCreate = async (request: PictureIn): Promise<Picture> => {
  const res = await apiFormClient.post(apiPictureCreate, request)
  if (res.status >= HttpStatusCode.BadRequest) throw Error
  return res.data
}

export const postBlogCreate = async (request: BlogIn): Promise<Blog> => {
  const res = await apiFormClient.post(apiBlogCreate, request)
  if (res.status >= HttpStatusCode.BadRequest) throw Error
  return res.data
}

export const postChatCreate = async (request: ChatIn): Promise<Chat> => {
  const res = await apiClient.post(apiChatCreate, request)
  if (res.status >= HttpStatusCode.BadRequest) throw Error
  return res.data
}

export const postTodoCreate = async (request: TodoIn): Promise<Todo> => {
  const res = await apiClient.post(apiTodoCreate, request)
  if (res.status >= HttpStatusCode.BadRequest) throw Error
  return res.data
}
