import { Channel } from 'types/internal/channel'
import { Video, Audio, Blog, Comic, Picture, Chat } from 'types/internal/media/output'

export interface UserPage {
  avatar: string
  banner: string
  nickname: string
  email: string
  content: string
  measurementId: string
  dateJoined: string
  followerCount: number
  followingCount: number
  isFollow: boolean
  channels: Channel[]
}

export interface UserPageMedia {
  videos: Video[]
  audios: Audio[]
  blogs: Blog[]
  comics: Comic[]
  pictures: Picture[]
  chats: Chat[]
}
