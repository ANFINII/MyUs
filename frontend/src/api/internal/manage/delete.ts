import { apiClient } from 'lib/axios/internal'
import { ApiOut, apiOut } from 'lib/error'
import { ErrorOut } from 'types/internal/other'
import { apiManageComics, apiManageMusics, apiManagePictures, apiManageVideos } from 'api/uri'

export const deleteManageVideos = async (ulids: string[]): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').delete(apiManageVideos, { data: { ulids } }))
}

export const deleteManageMusics = async (ulids: string[]): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').delete(apiManageMusics, { data: { ulids } }))
}

export const deleteManageComics = async (ulids: string[]): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').delete(apiManageComics, { data: { ulids } }))
}

export const deleteManagePictures = async (ulids: string[]): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').delete(apiManagePictures, { data: { ulids } }))
}
