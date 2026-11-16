<<<<<<< HEAD
import { Music } from 'types/internal/media/output'

=======
>>>>>>> origin/main
export interface PlaylistIn {
  title: string
  publish: boolean
  musicUlid: string
}

<<<<<<< HEAD
export interface PlaylistUpdateIn {
  title: string
  publish: boolean
  musicUlids: string[]
}

=======
>>>>>>> origin/main
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

<<<<<<< HEAD
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

=======
>>>>>>> origin/main
export interface PlaylistCreateOut {
  ulid: string
}
