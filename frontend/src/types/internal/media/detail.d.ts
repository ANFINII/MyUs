import { Comment } from 'types/internal/comment'
import { Author, MediaUser } from 'types/internal/media'
import { Video, Music, Comic, Picture, Blog, Chat } from 'types/internal/media'

export interface MediaDetail {
  id: number
  title: string
  content: string
  read: number
  likeCount: number
  publish: boolean
  created: Date
  updated: Date
  author: Author
  mediaUser: MediaUser
}

export interface VideoDetail extends MediaDetail {
  image: string
  video: string
  convert: string
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

export interface ChatDetail extends MediaDetail {
  read: number
  joined: number
  thread: number
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

export interface ChatDetailOut {
  detail: ChatDetail
  list: Chat[]
}
