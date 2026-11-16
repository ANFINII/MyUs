import { Music } from 'types/internal/media/output'

export interface PlaylistIn {
  title: string
  publish: boolean
  musicUlid: string
}

export interface PlaylistUpdateIn {
  title: string
  publish: boolean
  musicUlids: string[]
}

export interface PlaylistMusicIn {
  musicUlid: string
}

export interface Playlist {
  ulid: string
  title: string
  publish: boolean
  count: number
  image: string
  updated: string
}

export interface PlaylistList {
  items: Playlist[]
}

export interface PlaylistDetailOut {
  ulid: string
  title: string
  publish: boolean
  isOwner: boolean
  authorUlid: string
  authorNickname: string
  musics: Music[]
  updated: string
}

export interface PlaylistCreateOut {
  ulid: string
}
