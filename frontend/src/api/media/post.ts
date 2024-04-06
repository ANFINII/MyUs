import { HttpStatusCode } from 'axios'
import { apiClient, apiFormClient } from 'lib/axios'
import { apiPictureCreate, apiBlogCreate, apiChatCreate, apiComicCreate, apiVideoCreate, apiMusicCreate } from 'api/uri'
import { Video, Music, Comic, Picture, Blog, Chat } from 'types/internal/media'
import { VideoIn, MusicIn, ComicIn, PictureIn, BlogIn, ChatIn } from 'types/internal/media'

export const postVideoCreate = async (request: VideoIn) => {
  const data = await apiFormClient.post(apiVideoCreate, request).then((res) => {
    if (res.status !== HttpStatusCode.Created) throw Error
    return res.data as Video
  })
  return data
}

export const postMusicCreate = async (request: MusicIn) => {
  const data = await apiFormClient.post(apiMusicCreate, request).then((res) => {
    if (res.status !== HttpStatusCode.Created) throw Error
    return res.data as Music
  })
  return data
}

export const postComicCreate = async (request: ComicIn) => {
  const data = await apiFormClient.post(apiComicCreate, request).then((res) => {
    if (res.status !== HttpStatusCode.Created) throw Error
    return res.data as Comic
  })
  return data
}

export const postPictureCreate = async (request: PictureIn) => {
  const data = await apiFormClient.post(apiPictureCreate, request).then((res) => {
    if (res.status !== HttpStatusCode.Created) throw Error
    return res.data as Picture
  })
  return data
}

export const postBlogCreate = async (request: BlogIn) => {
  const data = await apiFormClient.post(apiBlogCreate, request).then((res) => {
    if (res.status !== HttpStatusCode.Created) throw Error
    return res.data as Blog
  })
  return data
}

export const postChatCreate = async (request: ChatIn) => {
  const data = await apiClient.post(apiChatCreate, request).then((res) => {
    if (res.status !== HttpStatusCode.Created) throw Error
    return res.data as Chat
  })
  return data
}
