import { apiClient } from 'lib/axios/internal'
import { cookieHeader } from 'lib/config'
import { ApiOut, apiOut } from 'lib/error'
import { Req } from 'types/global'
import { Video, Music, Comic, Picture, Chat, BlogDetailOut, FollowIn } from 'types/internal/media'
import { apiVideo, apiMusic, apiComic, apiPicture, apiBlog, apiChat, apiFollow } from 'api/uri'

export const getVideo = async (id: number, req?: Req): Promise<ApiOut<Video>> => {
  return await apiOut(apiClient.get(apiVideo(id), cookieHeader(req)))
}

export const getMusic = async (id: number, req?: Req): Promise<ApiOut<Music>> => {
  return await apiOut(apiClient.get(apiMusic(id), cookieHeader(req)))
}

export const getComic = async (id: number, req?: Req): Promise<ApiOut<Comic>> => {
  return await apiOut(apiClient.get(apiComic(id), cookieHeader(req)))
}

export const getPicture = async (id: number, req?: Req): Promise<ApiOut<Picture>> => {
  return await apiOut(apiClient.get(apiPicture(id), cookieHeader(req)))
}

export const getBlog = async (id: number, req?: Req): Promise<ApiOut<BlogDetailOut>> => {
  return await apiOut(apiClient.get(apiBlog(id), cookieHeader(req)))
}

export const getChat = async (id: number, req?: Req): Promise<ApiOut<Chat>> => {
  return await apiOut(apiClient.get(apiChat(id), cookieHeader(req)))
}

export const postFollow = async (request: FollowIn): Promise<ApiOut<void>> => {
  return await apiOut(apiClient.post(apiFollow, request))
}

export const deleteFollow = async (request: FollowIn): Promise<ApiOut<void>> => {
  return await apiOut(apiClient.delete(apiFollow, { data: request }))
}
