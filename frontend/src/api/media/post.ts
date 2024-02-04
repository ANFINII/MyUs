import { HttpStatusCode } from 'axios'
import { apiClient } from 'lib/axios'
import { apiPictureCreate } from 'api/uri'
import { CreatePcture, Picture } from 'types/internal/media'
import { snakeCamel } from 'utils/functions/convertCase'

export const postPictureCreate = async (request: CreatePcture) => {
  const data = await apiClient.post(apiPictureCreate, snakeCamel(request)).then((res) => {
    if (res.status !== HttpStatusCode.Created) throw Error
    return res.data as Picture
  })
  return data
}
