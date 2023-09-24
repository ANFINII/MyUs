import { Mypage } from 'types/internal/auth'

export interface Author {
  id: number
  nickname: string
  image: string
}

export interface Search {
  name: string
  count: number
}

export interface Media {
  id: number
  title: string
  content: string
  like: number
  read: number
  commentCount: number
  publish: boolean
  created: string
  updated: string
  author: Author
  modelName: string
}

export interface Video extends Media {
  image: string
  video: string
  convert: string
}

export interface Music extends Media {
  music: string
  lyric: string
  download: boolean
}

export interface Picture extends Media {
  image: string
}

export interface Chat extends Media {
  read: number
  joined: number
  thread: number
}

export interface Follow {
  id: number
  title: string
  content: string
  introduction: string
  like: number
  read: number
  commentCount: number
  publish: boolean
  created: string
  mypage: Mypage
  author: Author
}
