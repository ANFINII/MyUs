import { apiClient } from 'lib/axios/internal'
import { apiOut, ApiOut } from 'lib/error'
import { AdvertiseIn } from 'types/internal/advertise'
import { VideoIn, MusicIn, BlogIn, ComicIn, PictureIn, ChatIn } from 'types/internal/media/input'
import { MediaCreateOut } from 'types/internal/media/output'
import { apiManageAdvertises, apiVideos, apiMusics, apiBlogs, apiComics, apiPictures, apiChats } from 'api/uri'
import { camelSnake } from 'utils/functions/convertCase'

export const postVideoCreate = async (request: VideoIn): Promise<ApiOut<MediaCreateOut>> => {
  return await apiOut(apiClient('form').post(apiVideos, camelSnake(request)))
}

export const postMusicCreate = async (request: MusicIn): Promise<ApiOut<MediaCreateOut>> => {
  return await apiOut(apiClient('form').post(apiMusics, camelSnake(request)))
}

export const postBlogCreate = async (request: BlogIn): Promise<ApiOut<MediaCreateOut>> => {
  return await apiOut(apiClient('form').post(apiBlogs, camelSnake(request)))
}

export const postComicCreate = async (request: ComicIn): Promise<ApiOut<MediaCreateOut>> => {
  return await apiOut(apiClient('form').post(apiComics, camelSnake(request)))
}

export const postPictureCreate = async (request: PictureIn): Promise<ApiOut<MediaCreateOut>> => {
  return await apiOut(apiClient('form').post(apiPictures, camelSnake(request)))
}

export const postChatCreate = async (request: ChatIn): Promise<ApiOut<MediaCreateOut>> => {
  return await apiOut(apiClient('form').post(apiChats, camelSnake(request)))
}

export const postAdvertiseCreate = async (request: AdvertiseIn): Promise<ApiOut<MediaCreateOut>> => {
  return await apiOut(apiClient('form').post(apiManageAdvertises, camelSnake(request)))
}
