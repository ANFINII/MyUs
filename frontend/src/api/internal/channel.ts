import { apiClient } from 'lib/axios/internal'
import { cookieHeader } from 'lib/config'
import { ApiOut, apiOut } from 'lib/error'
import { Req } from 'types/global'
import { Channel, ChannelIn } from 'types/internal/channel'
import { ErrorOut } from 'types/internal/other'
import { apiChannel, apiChannels } from 'api/uri'
import { camelSnake } from 'utils/functions/convertCase'

export const getChannels = async (req?: Req): Promise<ApiOut<Channel[]>> => {
  return await apiOut(apiClient('json').get(apiChannels, cookieHeader(req)))
}

export const putChannel = async (ulid: string, request: ChannelIn): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('form').put(apiChannel(ulid), camelSnake(request)))
}
