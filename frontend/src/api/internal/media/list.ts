import { apiClient } from 'lib/axios/internal'
import { cookieHeader } from 'lib/config'
import { ApiOut, apiOut } from 'lib/error'
import { Req } from 'types/global'
import { SearchParms, MediaHome, Video, Music, Comic, Picture, Blog, Chat } from 'types/internal/media'
import { apiHome, apiVideos, apiMusics, apiComics, apiPictures, apiBlogs, apiChats } from 'api/uri'

export const getHome = async (params: SearchParms, req?: Req): Promise<ApiOut<MediaHome>> => {
  return await apiOut(apiClient.get(apiHome, cookieHeader(req, params)))
}

export const getVideos = async (params: SearchParms, req?: Req): Promise<ApiOut<Video[]>> => {
  return await apiOut(apiClient.get(apiVideos, cookieHeader(req, params)))
}

export const getMusics = async (params: SearchParms, req?: Req): Promise<ApiOut<Music[]>> => {
  return await apiOut(apiClient.get(apiMusics, cookieHeader(req, params)))
}

export const getComics = async (params: SearchParms, req?: Req): Promise<ApiOut<Comic[]>> => {
  return await apiOut(apiClient.get(apiComics, cookieHeader(req, params)))
}

export const getPictures = async (params: SearchParms, req?: Req): Promise<ApiOut<Picture[]>> => {
  return await apiOut(apiClient.get(apiPictures, cookieHeader(req, params)))
}

export const getBlogs = async (params: SearchParms, req?: Req): Promise<ApiOut<Blog[]>> => {
  return await apiOut(apiClient.get(apiBlogs, cookieHeader(req, params)))
}

export const getChats = async (params: SearchParms, req?: Req): Promise<ApiOut<Chat[]>> => {
  return await apiOut(apiClient.get(apiChats, cookieHeader(req, params)))
}
