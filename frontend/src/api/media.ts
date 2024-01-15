import { HttpStatusCode } from 'axios'
import { apiClient } from 'lib/axios'
import { apiVideos, apiMusics, apiComics, apiPictures, apiBlogs, apiChats, apiTodos } from './uri'

export const getVideos = async () => {
  const data = await apiClient.get(apiVideos).then((res) => {
    if (res.status !== HttpStatusCode.Ok) throw Error
    return res.data
  })
  return data
}

export const getMusics = async () => {
  const data = await apiClient.get(apiMusics).then((res) => {
    if (res.status !== HttpStatusCode.Ok) throw Error
    return res.data
  })
  return data
}

export const getComics = async () => {
  const data = await apiClient.get(apiComics).then((res) => {
    if (res.status !== HttpStatusCode.Ok) throw Error
    return res.data
  })
  return data
}

export const getPictures = async () => {
  const data = await apiClient.get(apiPictures).then((res) => {
    if (res.status !== HttpStatusCode.Ok) throw Error
    return res.data
  })
  return data
}

export const getBlogs = async () => {
  const data = await apiClient.get(apiBlogs).then((res) => {
    if (res.status !== HttpStatusCode.Ok) throw Error
    return res.data
  })
  return data
}

export const getChats = async () => {
  const data = await apiClient.get(apiChats).then((res) => {
    if (res.status !== HttpStatusCode.Ok) throw Error
    return res.data
  })
  return data
}

export const getTodos = async () => {
  const data = await apiClient.get(apiTodos).then((res) => {
    if (res.status !== HttpStatusCode.Ok) throw Error
    return res.data
  })
  return data
}
