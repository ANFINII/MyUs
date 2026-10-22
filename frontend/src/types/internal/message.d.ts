import { Author } from 'types/internal/user'

export interface ChatReplyOut {
  ulid: string
  text: string
  created: Date
  updated: Date
  author: Author
}

export interface ChatMessage extends ChatReplyOut {
  replyCount: number
}

export interface ChatReply extends ChatMessage {
  parentUlid: string
}

export interface MessageCreateIn {
  chatUlid: string
  text: string
  parentUlid?: string
}

export interface MessageUpdateIn {
  text: string
}
