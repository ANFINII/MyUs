import { apiClient } from 'lib/axios'
import { apiHome, apiVideos, apiMusics, apiComics, apiPictures, apiBlogs, apiChats, apiTodos } from 'api/uri'
import { MediaHome, Video, Music, Comic, Picture, Blog, Chat, Todo } from 'types/internal/media'

export const getHome = async () => {
  const data = await apiClient.get(apiHome).then((res) => {
    return res.data as MediaHome
  })
  return data
}

export const getVideos = async () => {
  const data = await apiClient.get(apiVideos).then((res) => {
    return res.data as Video[]
  })
  return data
}

export const getMusics = async () => {
  const data = await apiClient.get(apiMusics).then((res) => {
    return res.data as Music[]
  })
  return data
}

export const getComics = async () => {
  const data = await apiClient.get(apiComics).then((res) => {
    return res.data as Comic[]
  })
  return data
}

export const getPictures = async () => {
  const data = await apiClient.get(apiPictures).then((res) => {
    return res.data as Picture[]
  })
  return data
}

export const getBlogs = async () => {
  const data = await apiClient.get(apiBlogs).then((res) => {
    return res.data as Blog[]
  })
  return data
}

export const getChats = async () => {
  const data = await apiClient.get(apiChats).then((res) => {
    return res.data as Chat[]
  })
  return data
}

export const getTodos = async () => {
  const data = await apiClient.get(apiTodos).then((res) => {
    return res.data as Todo[]
  })
  return data
}
