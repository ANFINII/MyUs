import { apiClient } from 'lib/axios/internal'
import { ApiOut, apiOut } from 'lib/error'
import { VideoDetailOut, MusicDetailOut, BlogDetailOut, ComicDetailOut, PictureDetailOut, ChatDetailOut } from 'types/internal/media/output'
import { apiVideo, apiMusic, apiBlog, apiComic, apiPicture, apiChat } from 'api/uri'

export const getVideo = async (ulid: string): Promise<ApiOut<VideoDetailOut>> => {
  return await apiOut(apiClient('json').get(apiVideo(ulid)))
}

export const getMusic = async (ulid: string): Promise<ApiOut<MusicDetailOut>> => {
  return await apiOut(apiClient('json').get(apiMusic(ulid)))
}

export const getBlog = async (ulid: string): Promise<ApiOut<BlogDetailOut>> => {
  return await apiOut(apiClient('json').get(apiBlog(ulid)))
}

export const getComic = async (ulid: string): Promise<ApiOut<ComicDetailOut>> => {
  return await apiOut(apiClient('json').get(apiComic(ulid)))
}

export const getPicture = async (ulid: string): Promise<ApiOut<PictureDetailOut>> => {
  return await apiOut(apiClient('json').get(apiPicture(ulid)))
}

export const getChat = async (ulid: string): Promise<ApiOut<ChatDetailOut>> => {
  return await apiOut(apiClient('json').get(apiChat(ulid)))
}
