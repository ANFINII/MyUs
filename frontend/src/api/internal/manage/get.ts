import { apiClient } from 'lib/axios/internal'
import { cookieHeader } from 'lib/config'
import { ApiOut, apiOut } from 'lib/error'
import { Req } from 'types/global'
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
} from 'api/uri'

export const getManageVideos = async (params: SearchParams, req?: Req): Promise<ApiOut<VideoList>> => {
  return await apiOut(apiClient('json').get(apiManageVideos, cookieHeader(req, params)))
}

export const getManageMusics = async (params: SearchParams, req?: Req): Promise<ApiOut<MusicList>> => {
  return await apiOut(apiClient('json').get(apiManageMusics, cookieHeader(req, params)))
}

export const getManageBlogs = async (params: SearchParams, req?: Req): Promise<ApiOut<BlogList>> => {
  return await apiOut(apiClient('json').get(apiManageBlogs, cookieHeader(req, params)))
}

export const getManageComics = async (params: SearchParams, req?: Req): Promise<ApiOut<ComicList>> => {
  return await apiOut(apiClient('json').get(apiManageComics, cookieHeader(req, params)))
}

export const getManagePictures = async (params: SearchParams, req?: Req): Promise<ApiOut<PictureList>> => {
  return await apiOut(apiClient('json').get(apiManagePictures, cookieHeader(req, params)))
}

export const getManageChats = async (params: SearchParams, req?: Req): Promise<ApiOut<ChatList>> => {
  return await apiOut(apiClient('json').get(apiManageChats, cookieHeader(req, params)))
}

export const getManageVideo = async (ulid: string, req?: Req): Promise<ApiOut<Video>> => {
  return await apiOut(apiClient('json').get(apiManageVideo(ulid), cookieHeader(req)))
}

export const getManageMusic = async (ulid: string, req?: Req): Promise<ApiOut<Music>> => {
  return await apiOut(apiClient('json').get(apiManageMusic(ulid), cookieHeader(req)))
}

export const getManageBlog = async (ulid: string, req?: Req): Promise<ApiOut<Blog>> => {
  return await apiOut(apiClient('json').get(apiManageBlog(ulid), cookieHeader(req)))
}

export const getManageComic = async (ulid: string, req?: Req): Promise<ApiOut<Comic>> => {
  return await apiOut(apiClient('json').get(apiManageComic(ulid), cookieHeader(req)))
}

export const getManagePicture = async (ulid: string, req?: Req): Promise<ApiOut<Picture>> => {
  return await apiOut(apiClient('json').get(apiManagePicture(ulid), cookieHeader(req)))
}

export const getManageChat = async (ulid: string, req?: Req): Promise<ApiOut<Chat>> => {
  return await apiOut(apiClient('json').get(apiManageChat(ulid), cookieHeader(req)))
}
