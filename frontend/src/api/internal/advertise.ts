import { apiClient } from 'lib/axios/internal'
import { ApiOut, apiOut } from 'lib/error'
import { AdvertiseList } from 'types/internal/advertise'
import { apiAdvertiseRead, apiAdvertiseUser } from 'api/uri'

export const getUserAdvertises = async (userUlid: string): Promise<ApiOut<AdvertiseList>> => {
  return await apiOut(apiClient('json').get(apiAdvertiseUser(userUlid)))
}

export const postAdvertiseRead = async (ulid: string): Promise<ApiOut<{ read: number }>> => {
  return await apiOut(apiClient('json').post(apiAdvertiseRead(ulid)))
}
