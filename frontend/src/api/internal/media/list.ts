import { apiClient } from 'lib/axios/internal'
import { ApiOut, apiOut } from 'lib/error'
import { SearchParams, MediaHome, VideoList, MusicList, BlogList, ComicList, PictureList, ChatList } from 'types/internal/media/output'
import { apiHome, apiRecommend, apiVideos, apiMusics, apiBlogs, apiComics, apiPictures, apiChats } from 'api/uri'

export const getHome = async (params: SearchParams): Promise<ApiOut<MediaHome>> => {
  return await apiOut(apiClient('json').get(apiHome, { params }))
}

export const getRecommend = async (params: SearchParams): Promise<ApiOut<MediaHome>> => {
  return await apiOut(apiClient('json').get(apiRecommend, { params }))
}

export const getVideos = async (params: SearchParams): Promise<ApiOut<VideoList>> => {
  return await apiOut(apiClient('json').get(apiVideos, { params }))
}

export const getMusics = async (params: SearchParams): Promise<ApiOut<MusicList>> => {
  return await apiOut(apiClient('json').get(apiMusics, { params }))
}

export const getBlogs = async (params: SearchParams): Promise<ApiOut<BlogList>> => {
  return await apiOut(apiClient('json').get(apiBlogs, { params }))
}

export const getComics = async (params: SearchParams): Promise<ApiOut<ComicList>> => {
  return await apiOut(apiClient('json').get(apiComics, { params }))
}

export const getPictures = async (params: SearchParams): Promise<ApiOut<PictureList>> => {
  return await apiOut(apiClient('json').get(apiPictures, { params }))
}

export const getChats = async (params: SearchParams): Promise<ApiOut<ChatList>> => {
  return await apiOut(apiClient('json').get(apiChats, { params }))
}
