import { Video, Music, Comic, Picture, Blog, Chat } from 'types/internal/media'

export interface UserPage {
  avatar: string
  banner: string
  nickname: string
  content: string
  followerCount: number
  followingCount: number
  isFollow: boolean
  videos: Video[]
  musics: Music[]
  comics: Comic[]
  pictures: Picture[]
  blogs: Blog[]
  chats: Chat[]
}
