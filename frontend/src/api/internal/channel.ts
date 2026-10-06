import { apiClient } from 'lib/axios/internal'
import { ApiOut, apiOut } from 'lib/error'
import { Channel, ChannelCreateOut, ChannelIn, SubscribeIn, SubscribeOut } from 'types/internal/channel'
import { ErrorOut } from 'types/internal/other'
import { apiChannel, apiChannelCreate, apiChannelUser, apiChannelSubscribe } from 'api/uri'
import { camelSnake } from 'utils/functions/convertCase'

export const getChannels = async (): Promise<ApiOut<Channel[]>> => {
  return await apiOut(apiClient('json').get(apiChannelUser))
}

export const postChannel = async (request: ChannelIn): Promise<ApiOut<ChannelCreateOut>> => {
  return await apiOut(apiClient('form').post(apiChannelCreate, camelSnake(request)))
}

export const putChannel = async (ulid: string, request: ChannelIn): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('form').put(apiChannel(ulid), camelSnake(request)))
}

export const getSubscribeChannels = async (): Promise<ApiOut<Channel[]>> => {
  return await apiOut(apiClient('json').get(apiChannelSubscribe))
}

export const postSubscribeChannel = async (request: SubscribeIn): Promise<ApiOut<SubscribeOut>> => {
  return await apiOut(apiClient('json').post(apiChannelSubscribe, camelSnake(request)))
}
