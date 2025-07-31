import { apiClient } from 'lib/axios/internal'
import { cookieHeader } from 'lib/config'
import { ApiOut, apiOut } from 'lib/error'
import { Req } from 'types/global'
import { VideoDetailOut, MusicDetailOut, ComicDetailOut, PictureDetailOut, BlogDetailOut, ChatDetailOut } from 'types/internal/media/detail'
import { apiVideo, apiMusic, apiComic, apiPicture, apiBlog, apiChat } from 'api/uri'

export const getVideo = async (id: number, req?: Req): Promise<ApiOut<VideoDetailOut>> => {
  return await apiOut(apiClient.get(apiVideo(id), cookieHeader(req)))
}

export const getMusic = async (id: number, req?: Req): Promise<ApiOut<MusicDetailOut>> => {
  return await apiOut(apiClient.get(apiMusic(id), cookieHeader(req)))
}

export const getComic = async (id: number, req?: Req): Promise<ApiOut<ComicDetailOut>> => {
  return await apiOut(apiClient.get(apiComic(id), cookieHeader(req)))
}

export const getPicture = async (id: number, req?: Req): Promise<ApiOut<PictureDetailOut>> => {
  return await apiOut(apiClient.get(apiPicture(id), cookieHeader(req)))
}

export const getBlog = async (id: number, req?: Req): Promise<ApiOut<BlogDetailOut>> => {
  return await apiOut(apiClient.get(apiBlog(id), cookieHeader(req)))
}

export const getChat = async (id: number, req?: Req): Promise<ApiOut<ChatDetailOut>> => {
  return await apiOut(apiClient.get(apiChat(id), cookieHeader(req)))
}
