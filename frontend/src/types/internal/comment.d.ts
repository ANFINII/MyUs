import { CommentType, CommentTypeNo } from 'utils/constants/enum'
import { Author } from './media'

export interface Comment {
  ulid: string
  text: string
  created: Date
  updated: Date
  isCommentLike: boolean
  likeCount: number
  author: Author
  replys: Reply[]
}

export interface Reply {
  ulid: string
  text: string
  created: Date
  updated: Date
  isCommentLike: boolean
  likeCount: number
  author: Author
}

export interface CommnetIn {
  text: string
  typeName: CommentType
  typeNo: CommentTypeNo
  objectUlid: string
  parentUlid?: string
}

export interface CommentUpdateIn {
  text: string
}
