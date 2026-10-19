import { apiClient } from 'lib/axios/internal'
import { ApiOut, apiOut } from 'lib/error'
import { MediaReadIn } from 'types/internal/media/input'
import { MediaReadOut } from 'types/internal/media/output'
import { apiMediaRead } from 'api/uri'
import { camelSnake } from 'utils/functions/convertCase'

export const postMediaRead = async (request: MediaReadIn): Promise<ApiOut<MediaReadOut>> => {
  return await apiOut(apiClient('json').post(apiMediaRead, camelSnake(request)))
}

export const withMediaRead = async <T>(request: MediaReadIn, get: () => Promise<ApiOut<T>>): Promise<ApiOut<T>> => {
  await postMediaRead(request)
  return await get()
}
