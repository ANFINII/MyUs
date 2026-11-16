export interface PlaylistIn {
  title: string
  publish: boolean
  musicUlid: string
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

export interface PlaylistCreateOut {
  ulid: string
}
