import { apiClient } from 'lib/axios/internal'
import { cookieHeader } from 'lib/config'
import { ApiOut, apiOut } from 'lib/error'
import { Req } from 'types/global'
import { Comic, Music, SearchParams, Video } from 'types/internal/media/output'
import { apiManageComic, apiManageComics, apiManageMusic, apiManageMusics, apiManageVideo, apiManageVideos } from 'api/uri'

export const getManageVideos = async (params: SearchParams, req?: Req): Promise<ApiOut<Video[]>> => {
  return await apiOut(apiClient('json').get(apiManageVideos, cookieHeader(req, params)))
}

export const getManageMusics = async (params: SearchParams, req?: Req): Promise<ApiOut<Music[]>> => {
  return await apiOut(apiClient('json').get(apiManageMusics, cookieHeader(req, params)))
}

export const getManageComics = async (params: SearchParams, req?: Req): Promise<ApiOut<Comic[]>> => {
  return await apiOut(apiClient('json').get(apiManageComics, cookieHeader(req, params)))
}

export const getManageVideo = async (ulid: string, req?: Req): Promise<ApiOut<Video>> => {
  return await apiOut(apiClient('json').get(apiManageVideo(ulid), cookieHeader(req)))
}

export const getManageMusic = async (ulid: string, req?: Req): Promise<ApiOut<Music>> => {
  return await apiOut(apiClient('json').get(apiManageMusic(ulid), cookieHeader(req)))
}

export const getManageComic = async (ulid: string, req?: Req): Promise<ApiOut<Comic>> => {
  return await apiOut(apiClient('json').get(apiManageComic(ulid), cookieHeader(req)))
}
