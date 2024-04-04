import { Mypage } from 'types/internal/auth'

export interface Author {
  nickname: string
  image: string
  followerCount: number
}

export interface MediaUser {
  nickname: string
  image: string
  isLike: boolean
}

export interface Search {
  name: string
  count: number
}

export interface ToDo {
  id: number
  title: string
  content: string
  like: number
  read: number
  period: string
  publish: boolean
  created: string
  updated: string
  author: Author
}

export interface Media {
  id: number
  title: string
  content: string
  like: number
  read: number
  totalLike: number
  commentCount: number
  publish: boolean
  created: string
  updated: string
  author: Author
  user: MediaUser
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

export interface Comic extends Media {
  image: string
}

export interface Picture extends Media {
  image: string
}

export interface Blog extends Media {
  image: string
}

export interface Chat extends Media {
  read: number
  joined: number
  thread: number
}

export interface MediaDetail {
  id: number
  title: string
  content: string
  like: number
  read: number
  totalLike: number
  commentCount: number
  publish: boolean
  created: string
  updated: string
  author: Author
  user: MediaUser
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

export interface MediaHome {
  videos: Video[]
  musics: Music[]
  comics: Comic[]
  pictures: Picture[]
  blogs: Blog[]
  chats: Chat[]
}

// request
export interface ComicIn {
  title: string
  content: string
  image?: File
  images?: File[]
}

export interface PctureIn {
  title: string
  content: string
  image?: File
}

export interface BlogIn {
  title: string
  content: string
  image?: File
  richtext: string
}

export interface ChatIn {
  title: string
  content: string
  period: string
}

interface ToDoIn {
  title: string
  content: string
  priority: string
  progress: string
}
