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

export interface AudioIn extends MediaIn {
  lyric: string
  image?: File
  audio?: File
}

export interface BlogIn extends MediaIn {
  richtext: string
  paidText: string
  price: number
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
  video?: File
}

export interface AudioUpdateIn extends MediaUpdateIn {
  lyric: string
  image?: File
  audio?: File
}

export interface HiresIn {
  price: number
  hires?: File
}

export interface BlogUpdateIn extends MediaUpdateIn {
  richtext: string
  paidText: string
  price: number
  isPromotion: boolean
  image?: File
}

export interface ComicUpdateIn extends MediaUpdateIn {
  price: number
  freePages: number
  pages: string[]
  image?: File
  newPages?: File[]
}

export interface ComicPageItem {
  key: string
  src: string
  file: File | null
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
