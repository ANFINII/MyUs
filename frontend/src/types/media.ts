import { Mypage } from 'types/auth'

export interface Author {
  id: number
  nickname: string
  image: string
}

export interface SearchQuery {
  name: string
  count: number
}

export interface MediaResponse {
  id: number
  title: string
  content: string
  like: number
  read: number
  comment_count: number
  publish: boolean
  created: string
  updated: string
  author: Author
  modelName: string
}

export interface VideoResponse extends MediaResponse {
  image: string
  video: string
  convert: string
}

export interface MusicResponse extends MediaResponse {
  music: string
  lyric: string
  download: boolean
}

export interface ImageResponse extends MediaResponse {
  image: string
}

export interface ChatResponse extends MediaResponse {
  read: number
  joined: number
  thread: number
}

export interface FollowResponse {
  id: number
  title: string
  content: string
  introduction: string
  like: number
  read: number
  comment_count: number
  publish: boolean
  created: string
  mypage: Mypage
  author: Author
}
