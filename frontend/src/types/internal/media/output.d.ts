import { Channel } from 'types/internal/channel'
import { Comment } from 'types/internal/comment'
import { ChatMessage } from 'types/internal/message'
import { Product } from 'types/internal/payment'
import { EncodeStatus, HomeSort } from 'utils/constants/enum'

export interface Search {
  name?: string
  count: number
}

export interface SearchParams {
  search?: string
  limit?: number
  offset?: number
  channel?: string
  sort?: HomeSort
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
  publishAt: Date
  created: Date
  updated: Date
  categoryUlid: string
  channel: Channel
}

export interface Hashtag {
  ulid: string
  name: string
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
  encodeStatus: EncodeStatus
}

export interface Hires {
  sampleRate: number
  bitDepth: number
}

export interface Audio extends Media {
  image: string
  audio: string
  gain: number
  lyric: string
  hires: Hires | null
  product: Product | null
}

export interface HiresUrlOut {
  url: string
}

export interface Blog extends Media {
  richtext: string
  paidText: string
  isPromotion: boolean
  image: string
  product: Product | null
}

export interface Comic extends Media {
  image: string
  pages: string[]
  freePages: number
  product: Product | null
}

export interface Picture extends Media {
  image: string
}

export interface Chat extends Media {
  read: number
  joined: number
  thread: number
  period: Date
}

export interface MediaHome {
  videos: Video[]
  audios: Audio[]
  blogs: Blog[]
  comics: Comic[]
  pictures: Picture[]
  chats: Chat[]
}

export interface VideoList {
  items: Video[]
  total: number
}

export interface AudioList {
  items: Audio[]
  total: number
}

export interface BlogList {
  items: Blog[]
  total: number
}

export interface ComicList {
  items: Comic[]
  total: number
}

export interface PictureList {
  items: Picture[]
  total: number
}

export interface ChatList {
  items: Chat[]
  total: number
}

export interface VideoDetail extends MediaDetail {
  image: string
  video: string
  convert: string
  comments: Comment[]
}

export interface AudioDetail extends MediaDetail {
  image: string
  audio: string
  gain: number
  lyric: string
  isPurchased: boolean
  comments: Comment[]
  hires: Hires | null
  product: Product | null
}

export interface BlogDetail extends MediaDetail {
  richtext: string
  paidText: string
  isPurchased: boolean
  isPromotion: boolean
  image: string
  comments: Comment[]
  product: Product | null
}

export interface ComicDetail extends MediaDetail {
  image: string
  pageCount: number
  isPurchased: boolean
  pages: string[]
  comments: Comment[]
  product: Product | null
}

export interface PictureDetail extends MediaDetail {
  image: string
  comments: Comment[]
}

export interface ChatDetail extends MediaDetail {
  read: number
  joined: number
  thread: number
  period: Date
  messages: ChatMessage[]
}

export interface MediaSeries<T> {
  ulid: string
  title: string
  items: T[]
}

export interface VideoDetailOut {
  detail: VideoDetail
  list: Video[]
  series: MediaSeries<Video>
}

export interface AudioDetailOut {
  detail: AudioDetail
  list: Audio[]
  series: MediaSeries<Audio>
}

export interface BlogDetailOut {
  detail: BlogDetail
  list: Blog[]
  series: MediaSeries<Blog>
}

export interface ComicDetailOut {
  detail: ComicDetail
  list: Comic[]
  series: MediaSeries<Comic>
}

export interface PictureDetailOut {
  detail: PictureDetail
  list: Picture[]
  series: MediaSeries<Picture>
}

export interface ChatDetailOut {
  detail: ChatDetail
  list: Chat[]
  series: MediaSeries<Chat>
}

export interface MediaCreateOut {
  ulid: string
}

export interface MediaReadOut {
  read: number
}
