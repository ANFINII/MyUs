import { HttpStatusCode } from 'axios'
import { apiClient, apiFormClient } from 'lib/axios'
import { apiPictureCreate, apiBlogCreate, apiChatCreate, apiComicCreate } from 'api/uri'
import { Picture, Blog, Comic, ComicIn, PctureIn, BlogIn } from 'types/internal/media'

export const postComicCreate = async (request: ComicIn) => {
  const data = await apiFormClient.post(apiComicCreate, request).then((res) => {
    if (res.status !== HttpStatusCode.Created) throw Error
    return res.data as Comic
  })
  return data
}

export const postPictureCreate = async (request: PctureIn) => {
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

export const postChatCreate = async (request: any) => {
  const data = await apiClient.post(apiChatCreate, request).then((res) => {
    if (res.status !== HttpStatusCode.Created) throw Error
    return res.data as Blog
  })
  return data
}
