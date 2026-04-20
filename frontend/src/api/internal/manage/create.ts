import { apiClient } from 'lib/axios/internal'
import { apiOut, ApiOut } from 'lib/error'
import { VideoIn, MusicIn, BlogIn, ComicIn, PictureIn, ChatIn } from 'types/internal/media/input'
import { Video, Music, Blog, Comic, Picture, Chat } from 'types/internal/media/output'
import { apiVideos, apiMusics, apiBlogs, apiComics, apiPictures, apiChats } from 'api/uri'
import { camelSnake } from 'utils/functions/convertCase'

export const postVideoCreate = async (request: VideoIn): Promise<ApiOut<Video>> => {
  return await apiOut(apiClient('form').post(apiVideos, camelSnake(request)))
}

export const postMusicCreate = async (request: MusicIn): Promise<ApiOut<Music>> => {
  return await apiOut(apiClient('form').post(apiMusics, camelSnake(request)))
}

export const postBlogCreate = async (request: BlogIn): Promise<ApiOut<Blog>> => {
  return await apiOut(apiClient('form').post(apiBlogs, camelSnake(request)))
}

export const postComicCreate = async (request: ComicIn): Promise<ApiOut<Comic>> => {
  return await apiOut(apiClient('form').post(apiComics, camelSnake(request)))
}

export const postPictureCreate = async (request: PictureIn): Promise<ApiOut<Picture>> => {
  return await apiOut(apiClient('form').post(apiPictures, camelSnake(request)))
}

export const postChatCreate = async (request: ChatIn): Promise<ApiOut<Chat>> => {
  return await apiOut(apiClient('form').post(apiChats, camelSnake(request)))
}
