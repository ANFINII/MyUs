import { apiClient } from 'lib/axios'
import { apiVideo, apiMusic, apiComic, apiPicture, apiBlog, apiChat, apiTodo } from 'api/uri'
import { Video, Music, Comic, Picture, Blog, Chat, Todo } from 'types/internal/media'

export const getVideo = async (id: number) => {
  const data = await apiClient.get(apiVideo(id)).then((res) => {
    return res.data as Video
  })
  return data
}

export const getMusic = async (id: number) => {
  const data = await apiClient.get(apiMusic(id)).then((res) => {
    return res.data as Music
  })
  return data
}

export const getComic = async (id: number) => {
  const data = await apiClient.get(apiComic(id)).then((res) => {
    return res.data as Comic
  })
  return data
}

export const getPicture = async (id: number) => {
  const data = await apiClient.get(apiPicture(id)).then((res) => {
    return res.data as Picture
  })
  return data
}

export const getBlog = async (id: number) => {
  const data = await apiClient.get(apiBlog(id)).then((res) => {
    return res.data as Blog
  })
  return data
}

export const getChat = async (id: number) => {
  const data = await apiClient.get(apiChat(id)).then((res) => {
    return res.data as Chat
  })
  return data
}

export const getToDo = async (id: number) => {
  const data = await apiClient.get(apiTodo(id)).then((res) => {
    return res.data as Todo
  })
  return data
}
