import { Channel } from 'diagnostics_channel'
import { apiClient } from 'lib/axios/internal'
import { cookieHeader } from 'lib/config'
import { ApiOut, apiOut } from 'lib/error'
import { Req } from 'types/global'
import { apiChannel } from 'api/uri'

export const getChannels = async (req?: Req): Promise<ApiOut<Channel[]>> => {
  return await apiOut(apiClient('json').get(apiChannel, cookieHeader(req)))
}
