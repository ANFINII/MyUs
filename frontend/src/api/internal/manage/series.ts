import { apiClient } from 'lib/axios/internal'
import { ApiOut, apiOut } from 'lib/error'
import { ErrorOut } from 'types/internal/other'
import { SeriesCreateOut, SeriesDetail, SeriesIn, SeriesList, SeriesUpdateIn } from 'types/internal/series'
import { apiManageSeries, apiManageSeriesList } from 'api/uri'
import { camelSnake } from 'utils/functions/convertCase'

export const getManageSeriesList = async (channelUlid: string): Promise<ApiOut<SeriesList>> => {
  return await apiOut(apiClient('json').get(apiManageSeriesList, { params: camelSnake({ channelUlid }) }))
}

export const getManageSeries = async (ulid: string): Promise<ApiOut<SeriesDetail>> => {
  return await apiOut(apiClient('json').get(apiManageSeries(ulid)))
}

export const postManageSeries = async (request: SeriesIn): Promise<ApiOut<SeriesCreateOut>> => {
  return await apiOut(apiClient('json').post(apiManageSeriesList, camelSnake(request)))
}

export const putManageSeries = async (ulid: string, request: SeriesUpdateIn): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').put(apiManageSeries(ulid), camelSnake(request)))
}

export const deleteManageSeries = async (ulid: string): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').delete(apiManageSeries(ulid)))
}
