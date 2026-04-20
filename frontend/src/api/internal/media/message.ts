import { apiClient } from 'lib/axios/internal'
import { ApiOut, apiOut } from 'lib/error'
import { ChatMessage, MessageCreateIn, MessageUpdateIn } from 'types/internal/media/output'
import { apiMessages, apiMessage } from 'api/uri'
import { camelSnake } from 'utils/functions/convertCase'

export const postMessage = async (request: MessageCreateIn): Promise<ApiOut<ChatMessage>> => {
  return await apiOut(apiClient('json').post(apiMessages, camelSnake(request)))
}

export const getReplies = async (ulid: string): Promise<ApiOut<ChatMessage[]>> => {
  return await apiOut(apiClient('json').get(apiMessage(ulid)))
}

export const putMessage = async (ulid: string, request: MessageUpdateIn): Promise<ApiOut<void>> => {
  return await apiOut(apiClient('json').put(apiMessage(ulid), camelSnake(request)))
}

export const deleteMessage = async (ulid: string): Promise<ApiOut<void>> => {
  return await apiOut(apiClient('json').delete(apiMessage(ulid)))
}
