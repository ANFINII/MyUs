import { Audio } from 'types/internal/media/output'
import { Author } from 'types/internal/user'

export interface PlaylistIn {
  title: string
  publish: boolean
  audioUlid: string
}

export interface PlaylistUpdateIn {
  title: string
  description: string
  thumbnailAudioUlid: string
  publish: boolean
  audioUlids: string[]
}

export interface PlaylistAudioIn {
  audioUlid: string
}

export interface Playlist {
  ulid: string
  title: string
  image: string
  publish: boolean
  count: number
  audioUlids: string[]
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
  thumbnailAudioUlid: string
  publish: boolean
  isOwner: boolean
  updated: string
  author: Author
  audios: Audio[]
}

export interface PlaylistCreateOut {
  ulid: string
}
