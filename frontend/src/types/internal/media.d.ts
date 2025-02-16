export interface Author {
  avatar: string
  nickname: string
  followerCount: number
}

export interface MediaUser {
  avatar: string
  nickname: string
  isLike: boolean
  isFollow: boolean
}

export interface Search {
  name?: string
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
  richtext: string
}

export interface Chat extends Media {
  read: number
  joined: number
  thread: number
}

export interface BlogDetailOut {
  detail: Blog
  list: Blog[]
}

export interface MediaDetail {
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
  user: MediaUser
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
export interface SearchParms {
  search?: string
}

export interface VideoIn {
  title: string
  content: string
  image?: File
  video?: File
}

export interface MusicIn {
  title: string
  content: string
  lyric: string
  music?: File
  download: boolean
}

export interface ComicIn {
  title: string
  content: string
  image?: File
  images?: File[]
}

export interface PictureIn {
  title: string
  content: string
  image?: File
}

export interface BlogIn {
  title: string
  content: string
  richtext: string
  delta: string
  image?: File
}

export interface ChatIn {
  title: string
  content: string
  period: string
}

export interface CommnetIn {
  text: string
  type: string
}
