import { HttpStatusCode } from 'axios'
import { apiServer } from 'lib/apiServer'
import { apiClient } from 'lib/axios'
import { Req } from 'types/global/next'
import { apiAuth } from './uri'

export const getAuth = async (req: Req) => {
  const data = await apiServer(req, apiClient, apiAuth).then((res) => {
    return res.status === HttpStatusCode.Ok
  })
  return data
}
