import { Channel } from 'types/internal/channel'
import { Comment } from 'types/internal/comment'
import { MediaUser } from 'types/internal/media'
import { Video, Music, Comic, Picture, Blog, Chat } from 'types/internal/media'
import { Author } from 'types/internal/user'

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
  image: str
  richtext: str
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

export interface MessageCreateIn {
  chatUlid: string
  text: string
  parentUlid?: string
}

export interface MessageUpdateIn {
  chatUlid: string
  text: string
}
