import { apiClient } from 'lib/axios/internal'
import { ApiOut, apiOut } from 'lib/error'
import { Comment, CommnetIn, CommentUpdateIn } from 'types/internal/comment'
import { apiComments, apiComment, apiCommentLike } from 'api/uri'
import { camelSnake } from 'utils/functions/convertCase'

export const postComment = async (request: CommnetIn): Promise<ApiOut<Comment>> => {
  return await apiOut(apiClient.post(apiComments, camelSnake(request)))
}

export const putComment = async (id: number, request: CommentUpdateIn): Promise<ApiOut<void>> => {
  return await apiOut(apiClient.put(apiComment(id), request))
}

export const deleteComment = async (id: number): Promise<ApiOut<void>> => {
  return await apiOut(apiClient.delete(apiComment(id)))
}

export const postCommentLike = async (commentId: number): Promise<ApiOut<{ isCommentLike: boolean; totalLike: number }>> => {
  return await apiOut(apiClient.post(apiCommentLike, { commentId }))
}

export const deleteCommentLike = async (commentId: number): Promise<ApiOut<{ isCommentLike: boolean; totalLike: number }>> => {
  return await apiOut(apiClient.delete(apiCommentLike, { data: { commentId } }))
}
