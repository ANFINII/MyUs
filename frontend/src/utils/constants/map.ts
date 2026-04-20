import { GenderType, GenderView, CommentTypeNo, CommentType, MediaType } from 'utils/constants/enum'

export const genderMap: Record<GenderType, GenderView> = {
  [GenderType.Male]: GenderView.Male,
  [GenderType.Female]: GenderView.Female,
  [GenderType.Secret]: GenderView.Secret,
}

export const mediaTypeMap: Record<string, MediaType> = {
  Video: MediaType.Video,
  Music: MediaType.Music,
  Blog: MediaType.Blog,
  Comic: MediaType.Comic,
  Picture: MediaType.Picture,
}

export const commentTypeNoMap: Record<CommentType, CommentTypeNo> = {
  [CommentType.Video]: CommentTypeNo.Video,
  [CommentType.Music]: CommentTypeNo.Music,
  [CommentType.Blog]: CommentTypeNo.Blog,
  [CommentType.Comic]: CommentTypeNo.Comic,
  [CommentType.Picture]: CommentTypeNo.Picture,
}
