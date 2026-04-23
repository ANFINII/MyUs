import { apiClient } from 'lib/axios/internal'
import { cookieHeader } from 'lib/config'
import { ApiOut, apiOut } from 'lib/error'
import { Req } from 'types/global'
import { SearchParams, MediaHome, VideoList, MusicList, BlogList, ComicList, PictureList, ChatList } from 'types/internal/media/output'
import { apiHome, apiRecommend, apiVideos, apiMusics, apiBlogs, apiComics, apiPictures, apiChats } from 'api/uri'

export const getHome = async (params: SearchParams, req?: Req): Promise<ApiOut<MediaHome>> => {
  return await apiOut(apiClient('json').get(apiHome, cookieHeader(req, params)))
}

export const getRecommend = async (params: SearchParams, req?: Req): Promise<ApiOut<MediaHome>> => {
  return await apiOut(apiClient('json').get(apiRecommend, cookieHeader(req, params)))
}

export const getVideos = async (params: SearchParams, req?: Req): Promise<ApiOut<VideoList>> => {
  return await apiOut(apiClient('json').get(apiVideos, cookieHeader(req, params)))
}

export const getMusics = async (params: SearchParams, req?: Req): Promise<ApiOut<MusicList>> => {
  return await apiOut(apiClient('json').get(apiMusics, cookieHeader(req, params)))
}

export const getBlogs = async (params: SearchParams, req?: Req): Promise<ApiOut<BlogList>> => {
  return await apiOut(apiClient('json').get(apiBlogs, cookieHeader(req, params)))
}

export const getComics = async (params: SearchParams, req?: Req): Promise<ApiOut<ComicList>> => {
  return await apiOut(apiClient('json').get(apiComics, cookieHeader(req, params)))
}

export const getPictures = async (params: SearchParams, req?: Req): Promise<ApiOut<PictureList>> => {
  return await apiOut(apiClient('json').get(apiPictures, cookieHeader(req, params)))
}

export const getChats = async (params: SearchParams, req?: Req): Promise<ApiOut<ChatList>> => {
  return await apiOut(apiClient('json').get(apiChats, cookieHeader(req, params)))
}
