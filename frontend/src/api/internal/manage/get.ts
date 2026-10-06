import { apiClient } from 'lib/axios/internal'
import { ApiOut, apiOut } from 'lib/error'
import { Advertise, AdvertiseList, AdvertiseSearchParams } from 'types/internal/advertise'
import { VideoList, MusicList, BlogList, ComicList, PictureList, ChatList } from 'types/internal/media/output'
import { SearchParams, Video, Music, Blog, Comic, Picture, Chat } from 'types/internal/media/output'
import {
  apiManageVideos,
  apiManageVideo,
  apiManageMusics,
  apiManageMusic,
  apiManageBlogs,
  apiManageBlog,
  apiManageComics,
  apiManageComic,
  apiManagePictures,
  apiManagePicture,
  apiManageChats,
  apiManageChat,
  apiManageAdvertises,
  apiManageAdvertise,
} from 'api/uri'

export const getManageVideos = async (params: SearchParams): Promise<ApiOut<VideoList>> => {
  return await apiOut(apiClient('json').get(apiManageVideos, { params }))
}

export const getManageMusics = async (params: SearchParams): Promise<ApiOut<MusicList>> => {
  return await apiOut(apiClient('json').get(apiManageMusics, { params }))
}

export const getManageBlogs = async (params: SearchParams): Promise<ApiOut<BlogList>> => {
  return await apiOut(apiClient('json').get(apiManageBlogs, { params }))
}

export const getManageComics = async (params: SearchParams): Promise<ApiOut<ComicList>> => {
  return await apiOut(apiClient('json').get(apiManageComics, { params }))
}

export const getManagePictures = async (params: SearchParams): Promise<ApiOut<PictureList>> => {
  return await apiOut(apiClient('json').get(apiManagePictures, { params }))
}

export const getManageChats = async (params: SearchParams): Promise<ApiOut<ChatList>> => {
  return await apiOut(apiClient('json').get(apiManageChats, { params }))
}

export const getManageVideo = async (ulid: string): Promise<ApiOut<Video>> => {
  return await apiOut(apiClient('json').get(apiManageVideo(ulid)))
}

export const getManageMusic = async (ulid: string): Promise<ApiOut<Music>> => {
  return await apiOut(apiClient('json').get(apiManageMusic(ulid)))
}

export const getManageBlog = async (ulid: string): Promise<ApiOut<Blog>> => {
  return await apiOut(apiClient('json').get(apiManageBlog(ulid)))
}

export const getManageComic = async (ulid: string): Promise<ApiOut<Comic>> => {
  return await apiOut(apiClient('json').get(apiManageComic(ulid)))
}

export const getManagePicture = async (ulid: string): Promise<ApiOut<Picture>> => {
  return await apiOut(apiClient('json').get(apiManagePicture(ulid)))
}

export const getManageChat = async (ulid: string): Promise<ApiOut<Chat>> => {
  return await apiOut(apiClient('json').get(apiManageChat(ulid)))
}

export const getManageAdvertises = async (params: AdvertiseSearchParams): Promise<ApiOut<AdvertiseList>> => {
  return await apiOut(apiClient('json').get(apiManageAdvertises, { params }))
}

export const getManageAdvertise = async (ulid: string): Promise<ApiOut<Advertise>> => {
  return await apiOut(apiClient('json').get(apiManageAdvertise(ulid)))
}
