import { apiClient } from 'lib/axios/internal'
import { ApiOut, apiOut } from 'lib/error'
import { VideoDetailOut, AudioDetailOut, AudioHiresUrlOut, BlogDetailOut, ComicDetailOut, PictureDetailOut, ChatDetailOut } from 'types/internal/media/output'
import { apiVideo, apiAudio, apiAudioHires, apiBlog, apiComic, apiPicture, apiChat } from 'api/uri'

export const getVideo = async (ulid: string): Promise<ApiOut<VideoDetailOut>> => {
  return await apiOut(apiClient('json').get(apiVideo(ulid)))
}

export const getAudio = async (ulid: string): Promise<ApiOut<AudioDetailOut>> => {
  return await apiOut(apiClient('json').get(apiAudio(ulid)))
}

export const getAudioHiresUrl = async (ulid: string): Promise<ApiOut<AudioHiresUrlOut>> => {
  return await apiOut(apiClient('json').get(apiAudioHires(ulid)))
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
