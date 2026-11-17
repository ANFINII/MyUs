import { Music } from 'types/internal/media/output'
import { Author } from 'types/internal/user'

export interface PlaylistIn {
  title: string
  publish: boolean
  musicUlid: string
}

export interface PlaylistUpdateIn {
  title: string
  description: string
  thumbnailMusicUlid: string
  publish: boolean
  musicUlids: string[]
}

export interface PlaylistMusicIn {
  musicUlid: string
}

export interface Playlist {
  ulid: string
  title: string
  image: string
  publish: boolean
  count: number
  musicUlids: string[]
  updated: string
}

export interface PlaylistList {
  items: Playlist[]
}

export interface PlaylistDetailOut {
  ulid: string
  title: string
  description: string
  image: string
  thumbnailMusicUlid: string
  publish: boolean
  isOwner: boolean
  updated: string
  author: Author
  musics: Music[]
}

export interface PlaylistCreateOut {
  ulid: string
}
