import { GenderType, GenderView, CommentTypeNo, CommentType } from 'utils/constants/enum'

export const genderMap: Record<GenderType, GenderView> = {
  [GenderType.Male]: GenderView.Male,
  [GenderType.Female]: GenderView.Female,
  [GenderType.Secret]: GenderView.Secret,
}

export const commentTypeNoMap: Record<CommentType, CommentTypeNo> = {
  [CommentType.Video]: CommentTypeNo.Video,
  [CommentType.Music]: CommentTypeNo.Music,
  [CommentType.Comic]: CommentTypeNo.Comic,
  [CommentType.Picture]: CommentTypeNo.Picture,
  [CommentType.Blog]: CommentTypeNo.Blog,
}
