export interface MediaIn {
  channelUlid: string
  categoryUlid: string
  publish: boolean
  title: string
  content: string
}

export interface VideoIn extends MediaIn {
  image?: File
  video?: File
}

export interface MusicIn extends MediaIn {
  lyric: string
  download: boolean
  music?: File
}

export interface BlogIn extends MediaIn {
  richtext: string
  delta: string
  image?: File
}

export interface ComicIn extends MediaIn {
  image?: File
  pages?: File[]
}

export interface PictureIn extends MediaIn {
  image?: File
}

export interface ChatIn extends MediaIn {
  period: string
}

export interface MediaUpdateIn {
  categoryUlid: string
  title: string
  content: string
  publish: boolean
}

export interface VideoUpdateIn extends MediaUpdateIn {
  image?: File
}

export interface MusicUpdateIn extends MediaUpdateIn {
  lyric: string
  download: boolean
}

export interface BlogUpdateIn extends MediaUpdateIn {
  richtext: string
  image?: File
}

export interface ComicUpdateIn extends MediaUpdateIn {
  image?: File
}

export interface PictureUpdateIn extends MediaUpdateIn {
  image?: File
}

export interface ChatUpdateIn extends MediaUpdateIn {
  period: string
}
