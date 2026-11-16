import { apiClient } from 'lib/axios/internal'
import { ApiOut, apiOut } from 'lib/error'
import { ChannelSeriesList } from 'types/internal/series'
import { apiChannelSeries } from 'api/uri'

export const getChannelSeries = async (channelUlid: string): Promise<ApiOut<ChannelSeriesList>> => {
  return await apiOut(apiClient('json').get(apiChannelSeries(channelUlid)))
}
