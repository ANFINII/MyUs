import { Author } from './media'

export interface Comment {
  id: number
  text: string
  created: Date
  updated: Date
  replys: Reply[]
  author: Author
  isCommentLike?: boolean
  likeCount: number
}

export interface Reply {
  id: number
  text: string
  created: Date
  updated: Date
  author: Author
  isCommentLike?: boolean
  likeCount: number
}

export interface CommnetIn {
  text: string
  typeName: CommentType
  typeNo: CommentTypeNo
  objectId: number
  parentId?: number
}

export interface CommentUpdateIn {
  text: string
}
