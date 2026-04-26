import { apiClient } from 'lib/axios/internal'
import { ApiOut, apiOut } from 'lib/error'
import { MediaHashtagsUpdateIn } from 'types/internal/hashtag'
import { ErrorOut } from 'types/internal/other'
import { apiMediaHashtag } from 'api/uri'
import { camelSnake } from 'utils/functions/convertCase'

export const putMediaHashtags = async (request: MediaHashtagsUpdateIn): Promise<ApiOut<ErrorOut>> => {
  return await apiOut(apiClient('json').put(apiMediaHashtag, camelSnake(request)))
}
