import { Author } from './media'

export interface Comment {
  id: number
  text: string
  created: Date
  updated: Date
  replys: Reply[]
  author: Author
  isCommentLike?: boolean
  totalLike?: number
}

export interface Reply {
  id: number
  text: string
  created: Date
  updated: Date
  author: Author
  totalLike?: number
}
