import { MediaType } from 'utils/constants/enum'

export interface MediaIn {
  channelUlid: string
  categoryUlid: string
  publish: boolean
  publishAt: string
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
  isPromotion: boolean
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
  publishAt: string
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
  isPromotion: boolean
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

export interface MediaReadIn {
  ulid: string
  mediaType: MediaType
}
