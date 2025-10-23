import { apiClient } from 'lib/axios/internal'
import { cookieHeader } from 'lib/config'
import { ApiOut, apiOut } from 'lib/error'
import { Req } from 'types/global'
import { VideoDetailOut, MusicDetailOut, ComicDetailOut, PictureDetailOut, BlogDetailOut, ChatDetailOut } from 'types/internal/media/detail'
import { apiVideo, apiMusic, apiComic, apiPicture, apiBlog, apiChat } from 'api/uri'

export const getVideo = async (ulid: string, req?: Req): Promise<ApiOut<VideoDetailOut>> => {
  return await apiOut(apiClient('json').get(apiVideo(ulid), cookieHeader(req)))
}

export const getMusic = async (ulid: string, req?: Req): Promise<ApiOut<MusicDetailOut>> => {
  return await apiOut(apiClient('json').get(apiMusic(ulid), cookieHeader(req)))
}

export const getComic = async (ulid: string, req?: Req): Promise<ApiOut<ComicDetailOut>> => {
  return await apiOut(apiClient('json').get(apiComic(ulid), cookieHeader(req)))
}

export const getPicture = async (ulid: string, req?: Req): Promise<ApiOut<PictureDetailOut>> => {
  return await apiOut(apiClient('json').get(apiPicture(ulid), cookieHeader(req)))
}

export const getBlog = async (ulid: string, req?: Req): Promise<ApiOut<BlogDetailOut>> => {
  return await apiOut(apiClient('json').get(apiBlog(ulid), cookieHeader(req)))
}

export const getChat = async (ulid: string, req?: Req): Promise<ApiOut<ChatDetailOut>> => {
  return await apiOut(apiClient('json').get(apiChat(ulid), cookieHeader(req)))
}
