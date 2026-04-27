export interface VideoIn {
  channelUlid: string
  categoryUlid: string
  publish: boolean
  title: string
  content: string
  image?: File
  video?: File
}

export interface MusicIn {
  channelUlid: string
  categoryUlid: string
  publish: boolean
  title: string
  content: string
  lyric: string
  download: boolean
  music?: File
}

export interface BlogIn {
  channelUlid: string
  categoryUlid: string
  publish: boolean
  title: string
  content: string
  richtext: string
  delta: string
  image?: File
}

export interface ComicIn {
  channelUlid: string
  categoryUlid: string
  publish: boolean
  title: string
  content: string
  image?: File
  pages?: File[]
}

export interface PictureIn {
  channelUlid: string
  categoryUlid: string
  publish: boolean
  title: string
  content: string
  image?: File
}

export interface ChatIn {
  channelUlid: string
  categoryUlid: string
  publish: boolean
  title: string
  content: string
  period: string
}

export interface VideoUpdateIn {
  title: string
  content: string
  publish: boolean
  image?: File
}

export interface MusicUpdateIn {
  title: string
  content: string
  lyric: string
  download: boolean
  publish: boolean
}

export interface BlogUpdateIn {
  title: string
  content: string
  richtext: string
  publish: boolean
  image?: File
}

export interface ComicUpdateIn {
  title: string
  content: string
  publish: boolean
  image?: File
}

export interface PictureUpdateIn {
  title: string
  content: string
  publish: boolean
  image?: File
}

export interface ChatUpdateIn {
  title: string
  content: string
  period: string
  publish: boolean
}
