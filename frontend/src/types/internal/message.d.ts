import { Author } from 'types/internal/user'

export interface MessageCreateIn {
  chatUlid: string
  text: string
  parentUlid?: string
}

export interface MessageUpdateIn {
  chatUlid: string
  text: string
}

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
