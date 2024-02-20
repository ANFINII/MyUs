import { HttpStatusCode } from 'axios'
import { apiClient, apiFormClient } from 'lib/axios'
import { apiPictureCreate, apiBlogCreate, apiChatCreate } from 'api/uri'
import { Picture, Blog, CreatePcture } from 'types/internal/media'
import { snakeCamel } from 'utils/functions/convertCase'

export const postPictureCreate = async (request: CreatePcture) => {
  const data = await apiFormClient.post(apiPictureCreate, snakeCamel(request)).then((res) => {
    if (res.status !== HttpStatusCode.Created) throw Error
    return res.data as Picture
  })
  return data
}

export const postBlogCreate = async (formData: any) => {
  const data = await apiFormClient.post(apiBlogCreate, formData).then((res) => {
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
