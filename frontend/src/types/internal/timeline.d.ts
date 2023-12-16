import { User } from 'types/internal/auth'

export interface FileType {
  src: string
  name: string
  isImage: boolean
}

export interface EmailHistory {
  subject: string
  text: string
}

export interface MentionUser {
  id: number
  value: string
  avatar: string
}

export interface Timeline {
  id: number
  type: number
  content: string
  subContent?: string
  createdAt: string
  user: User | null
  files: FileType[] | File[]
  emailHistory: EmailHistory | null
}

export interface TimelineGroups {
  [status: string]: Timeline[]
}

export interface TimelineCommentState {
  id: number
  content: string
}

export interface TimelineCommentRequest {
  type: number
  content: string
  fileUrls: File[]
  mentionUserIds: number[]
}
