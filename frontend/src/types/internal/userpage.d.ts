import { Channel } from 'types/internal/channel'
import { Video, Music, Comic, Picture, Blog, Chat } from 'types/internal/media/output'

export interface UserPage {
  avatar: string
  banner: string
  nickname: string
  email: string
  content: string
  dateJoined: string
  followerCount: number
  followingCount: number
  isFollow: boolean
  channels: Channel[]
}

export interface UserPageMedia {
  videos: Video[]
  musics: Music[]
  comics: Comic[]
  pictures: Picture[]
  blogs: Blog[]
  chats: Chat[]
}
