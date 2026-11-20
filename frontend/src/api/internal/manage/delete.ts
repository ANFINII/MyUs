import { apiClient } from 'lib/axios/internal'
import { ApiOut, apiOut } from 'lib/error'
import { ErrorOut } from 'types/internal/other'
import { apiManageVideos, apiManageAudios, apiManageHires, apiManageBlogs, apiManageComics, apiManagePictures, apiManageChats, apiManageAdvertises } from 'api/uri'

export const deleteManageVideos = async (ulids: string[]): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').delete(apiManageVideos, { data: { ulids } }))
}

export const deleteManageAudios = async (ulids: string[]): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').delete(apiManageAudios, { data: { ulids } }))
}

export const deleteManageHires = async (ulid: string): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').delete(apiManageHires(ulid)))
}

export const deleteManageBlogs = async (ulids: string[]): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').delete(apiManageBlogs, { data: { ulids } }))
}

export const deleteManageComics = async (ulids: string[]): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').delete(apiManageComics, { data: { ulids } }))
}

export const deleteManagePictures = async (ulids: string[]): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').delete(apiManagePictures, { data: { ulids } }))
}

export const deleteManageChats = async (ulids: string[]): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').delete(apiManageChats, { data: { ulids } }))
}

export const deleteManageAdvertises = async (ulids: string[]): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').delete(apiManageAdvertises, { data: { ulids } }))
}
