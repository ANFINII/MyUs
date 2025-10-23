import { apiClient } from 'lib/axios/internal'
import { apiOut, ApiOut } from 'lib/error'
import { Video, Music, Comic, Picture, Blog, Chat } from 'types/internal/media'
import { VideoIn, MusicIn, ComicIn, PictureIn, BlogIn, ChatIn } from 'types/internal/media'
import { apiVideoCreate, apiMusicCreate, apiComicCreate, apiPictureCreate, apiBlogCreate, apiChatCreate } from 'api/uri'

export const postVideoCreate = async (request: VideoIn): Promise<ApiOut<Video>> => {
  return await apiOut(apiClient('form').post(apiVideoCreate, request))
}

export const postMusicCreate = async (request: MusicIn): Promise<ApiOut<Music>> => {
  return await apiOut(apiClient('form').post(apiMusicCreate, request))
}

export const postComicCreate = async (request: ComicIn): Promise<ApiOut<Comic>> => {
  return await apiOut(apiClient('form').post(apiComicCreate, request))
}

export const postPictureCreate = async (request: PictureIn): Promise<ApiOut<Picture>> => {
  return await apiOut(apiClient('form').post(apiPictureCreate, request))
}

export const postBlogCreate = async (request: BlogIn): Promise<ApiOut<Blog>> => {
  return await apiOut(apiClient('form').post(apiBlogCreate, request))
}

export const postChatCreate = async (request: ChatIn): Promise<ApiOut<Chat>> => {
  return await apiOut(apiClient('form').post(apiChatCreate, request))
}
