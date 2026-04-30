import { apiClient } from 'lib/axios/internal'
import { cookieHeader } from 'lib/config'
import { ApiOut, apiOut } from 'lib/error'
import { Req } from 'types/global'
import { AdvertiseList } from 'types/internal/advertise'
import { apiAdvertiseRead, apiAdvertiseUser } from 'api/uri'

export const getUserAdvertises = async (userUlid: string, req?: Req): Promise<ApiOut<AdvertiseList>> => {
  return await apiOut(apiClient('json').get(apiAdvertiseUser(userUlid), cookieHeader(req)))
}

export const postAdvertiseRead = async (ulid: string): Promise<ApiOut<{ read: number }>> => {
  return await apiOut(apiClient('json').post(apiAdvertiseRead(ulid)))
}
