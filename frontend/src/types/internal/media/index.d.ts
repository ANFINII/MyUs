import { Channel } from 'types/internal/channel'

export interface Search {
  name?: string
  count: number
}

export interface SearchParms {
  search?: string
}

export interface MediaUser {
  isLike: boolean
  isSubscribe: boolean
}

export interface Media {
  ulid: string
  title: string
  content: string
  read: number
  like: number
  publish: boolean
  created: Date
  updated: Date
  channel: Channel
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
