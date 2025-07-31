import { Comment } from './comment'

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
  id: number
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

export interface FollowIn {
  ulid: string
  isFollow: boolean
}

export interface FollowOut {
  isFollow: boolean
  followerCount: number
}

export interface MediaDetail {
  id: number
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

export interface VideoDetail extends Video {
  comments: Comment[]
  hashtags: string[]
}

export interface MusicDetail extends Music {
  comments: Comment[]
  hashtags: string[]
}

export interface ComicDetail extends Comic {
  comments: Comment[]
  hashtags: string[]
}

export interface PictureDetail extends Picture {
  comments: Comment[]
  hashtags: string[]
}

export interface BlogDetail extends MediaDetail {
  image: str
  richtext: str
  comments: Comment[]
  hashtags: string[]
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
