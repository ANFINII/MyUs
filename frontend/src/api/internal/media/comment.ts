import { apiClient } from 'lib/axios/internal'
import { ApiOut, apiOut } from 'lib/error'
import { Comment, CommnetIn, CommentUpdateIn } from 'types/internal/comment'
import { apiComments, apiComment } from 'api/uri'
import { camelSnake } from 'utils/functions/convertCase'

export const postComment = async (request: CommnetIn): Promise<ApiOut<Comment>> => {
  return await apiOut(apiClient('json').post(apiComments, camelSnake(request)))
}

export const putComment = async (ulid: string, request: CommentUpdateIn): Promise<ApiOut<void>> => {
  return await apiOut(apiClient('json').put(apiComment(ulid), request))
}

export const deleteComment = async (ulid: string): Promise<ApiOut<void>> => {
  return await apiOut(apiClient('json').delete(apiComment(ulid)))
}
