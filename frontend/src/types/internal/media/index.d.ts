export interface Author {
  avatar: string
  ulid: string
  nickname: string
  followerCount: number
}

export interface MediaUser {
  isLike: boolean
  isFollow: boolean
}

export interface NotificationUser {
  avatar: string
  ulid: string
  nickname: string
}

export interface Search {
  name?: string
  count: number
}

export interface Media {
  ulid: string
  title: string
  content: string
  like: number
  read: number
  publish: boolean
  created: Date
  updated: Date
  author: Author
  mediaUser: MediaUser
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
  channelUlid: string
  title: string
  content: string
  image?: File
  video?: File
}

export interface MusicIn {
  channelUlid: string
  title: string
  content: string
  lyric: string
  download: boolean
  music?: File
}

export interface ComicIn {
  channelUlid: string
  title: string
  content: string
  image?: File
  images?: File[]
}

export interface PictureIn {
  channelUlid: string
  title: string
  content: string
  image?: File
}

export interface BlogIn {
  channelUlid: string
  title: string
  content: string
  richtext: string
  delta: string
  image?: File
}

export interface ChatIn {
  channelUlid: string
  title: string
  content: string
  period: string
}
