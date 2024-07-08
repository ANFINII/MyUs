import { apiClient } from 'lib/axios'
import { apiHome, apiVideos, apiMusics, apiComics, apiPictures, apiBlogs, apiChats, apiTodos } from 'api/uri'
import { MediaHome, Video, Music, Comic, Picture, Blog, Chat, Todo } from 'types/internal/media'

export const getHome = async (search?: string) => {
  const data = await apiClient.get(apiHome, { params: { search } }).then((res) => {
    return res.data as MediaHome
  })
  return data
}

export const getVideos = async (search?: string) => {
  const data = await apiClient.get(apiVideos, { params: { search } }).then((res) => {
    return res.data as Video[]
  })
  return data
}

export const getMusics = async (search?: string) => {
  const data = await apiClient.get(apiMusics, { params: { search } }).then((res) => {
    return res.data as Music[]
  })
  return data
}

export const getComics = async (search?: string) => {
  const data = await apiClient.get(apiComics, { params: { search } }).then((res) => {
    return res.data as Comic[]
  })
  return data
}

export const getPictures = async (search?: string) => {
  const data = await apiClient.get(apiPictures, { params: { search } }).then((res) => {
    return res.data as Picture[]
  })
  return data
}

export const getBlogs = async (search?: string): Promise<Blog[]> => {
  const data = await apiClient.get(apiBlogs, { params: { search } }).then((res) => {
    return res.data as Blog[]
  })
  return data
}

export const getChats = async (search?: string) => {
  const data = await apiClient.get(apiChats).then((res) => {
    return res.data as Chat[]
  })
  return data
}

export const getTodos = async (search?: string) => {
  const data = await apiClient.get(apiTodos, { params: { search } }).then((res) => {
    return res.data as Todo[]
  })
  return data
}
