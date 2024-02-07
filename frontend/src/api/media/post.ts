import { HttpStatusCode } from 'axios'
import { apiFormClient } from 'lib/axios'
import { apiPictureCreate, apiBlogCreate } from 'api/uri'
import { Picture, Blog, CreatePcture, CreateBlog } from 'types/internal/media'
import { snakeCamel } from 'utils/functions/convertCase'

export const postPictureCreate = async (request: CreatePcture) => {
  const data = await apiFormClient.post(apiPictureCreate, snakeCamel(request)).then((res) => {
    if (res.status !== HttpStatusCode.Created) throw Error
    return res.data as Picture
  })
  return data
}

export const postBlogCreate = async (request: CreateBlog) => {
  const data = await apiFormClient.post(apiBlogCreate, snakeCamel(request)).then((res) => {
    if (res.status !== HttpStatusCode.Created) throw Error
    return res.data as Blog
  })
  return data
}
