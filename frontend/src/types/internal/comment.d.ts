import { Author } from './media'

export interface Comment {
  id: number
  text: string
  created: Date
  updated: Date
  isCommentLike: boolean
  likeCount: number
  author: Author
  replys: Reply[]
}

export interface Reply {
  id: number
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
  objectId: number
  parentId?: number
}

export interface CommentUpdateIn {
  text: string
}
