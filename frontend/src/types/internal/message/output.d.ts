import { Author } from 'types/internal/user'

export interface ChatMessage {
  ulid: string
  text: string
  replyCount: number
  created: Date
  updated: Date
  author: Author
}

export interface ChatReply extends ChatMessage {
  parentUlid: string
}
