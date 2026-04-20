import { Channel } from 'types/internal/channel'
import { Comment } from 'types/internal/comment'
import { ChatMessage } from 'types/internal/message'

export interface Search {
  name?: string
  count: number
}

export interface SearchParams {
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

export interface Hashtag {
  jpName: string
}

export interface MediaDetail {
  ulid: string
  title: string
  content: string
  read: number
  like: number
  publish: boolean
  created: Date
  updated: Date
  channel: Channel
  hashtags: Hashtag[]
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
  period: Date
}

export interface MediaHome {
  videos: Video[]
  musics: Music[]
  comics: Comic[]
  pictures: Picture[]
  blogs: Blog[]
  chats: Chat[]
}

export interface VideoDetail extends MediaDetail {
  image: string
  video: string
  convert: string
  comments: Comment[]
}

export interface MusicDetail extends MediaDetail {
  music: string
  lyric: string
  download: boolean
  comments: Comment[]
}

export interface ComicDetail extends MediaDetail {
  image: string
  pages: string[]
  comments: Comment[]
}

export interface PictureDetail extends MediaDetail {
  image: string
  comments: Comment[]
}

export interface BlogDetail extends MediaDetail {
  image: string
  richtext: string
  comments: Comment[]
}

export interface ChatDetail extends MediaDetail {
  read: number
  joined: number
  thread: number
  period: Date
  messages: ChatMessage[]
}

export interface VideoDetailOut {
  detail: VideoDetail
  list: Video[]
}

export interface MusicDetailOut {
  detail: MusicDetail
  list: Music[]
}

export interface ComicDetailOut {
  detail: ComicDetail
  list: Comic[]
}

export interface PictureDetailOut {
  detail: PictureDetail
  list: Picture[]
}

export interface BlogDetailOut {
  detail: BlogDetail
  list: Blog[]
}

export interface ChatDetailOut {
  detail: ChatDetail
  list: Chat[]
}
