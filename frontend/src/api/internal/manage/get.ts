import { apiClient } from 'lib/axios/internal'
import { cookieHeader } from 'lib/config'
import { ApiOut, apiOut } from 'lib/error'
import { Req } from 'types/global'
import { Blog, Comic, Music, Picture, SearchParams, Video } from 'types/internal/media/output'
import { apiManageBlog, apiManageBlogs, apiManageComic, apiManageComics, apiManageMusic, apiManageMusics, apiManagePicture, apiManagePictures, apiManageVideo, apiManageVideos } from 'api/uri'

export const getManageVideos = async (params: SearchParams, req?: Req): Promise<ApiOut<Video[]>> => {
  return await apiOut(apiClient('json').get(apiManageVideos, cookieHeader(req, params)))
}

export const getManageMusics = async (params: SearchParams, req?: Req): Promise<ApiOut<Music[]>> => {
  return await apiOut(apiClient('json').get(apiManageMusics, cookieHeader(req, params)))
}

export const getManageComics = async (params: SearchParams, req?: Req): Promise<ApiOut<Comic[]>> => {
  return await apiOut(apiClient('json').get(apiManageComics, cookieHeader(req, params)))
}

export const getManagePictures = async (params: SearchParams, req?: Req): Promise<ApiOut<Picture[]>> => {
  return await apiOut(apiClient('json').get(apiManagePictures, cookieHeader(req, params)))
}

export const getManageBlogs = async (params: SearchParams, req?: Req): Promise<ApiOut<Blog[]>> => {
  return await apiOut(apiClient('json').get(apiManageBlogs, cookieHeader(req, params)))
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

export const getManagePicture = async (ulid: string, req?: Req): Promise<ApiOut<Picture>> => {
  return await apiOut(apiClient('json').get(apiManagePicture(ulid), cookieHeader(req)))
}

export const getManageBlog = async (ulid: string, req?: Req): Promise<ApiOut<Blog>> => {
  return await apiOut(apiClient('json').get(apiManageBlog(ulid), cookieHeader(req)))
}
