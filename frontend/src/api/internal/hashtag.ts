import { apiClient } from 'lib/axios/internal'
import { cookieHeader } from 'lib/config'
import { ApiOut, apiOut } from 'lib/error'
import { Req } from 'types/global'
import { HashtagOut, MediaHashtagsUpdateIn } from 'types/internal/hashtag'
import { ErrorOut } from 'types/internal/other'
import { apiMediaHashtag } from 'api/uri'
import { camelSnake } from 'utils/functions/convertCase'

export const getHashtags = async (req?: Req): Promise<ApiOut<HashtagOut[]>> => {
  return await apiOut(apiClient('json').get(apiMediaHashtag, cookieHeader(req)))
}

export const putMediaHashtags = async (request: MediaHashtagsUpdateIn): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').put(apiMediaHashtag, camelSnake(request)))
}
