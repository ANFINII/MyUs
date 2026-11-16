import { MediaType } from 'utils/constants/enum'

export interface SeriesIn {
  channelUlid: string
  mediaType: MediaType
  title: string
}

export interface SeriesUpdateIn {
  title: string
  mediaUlids: string[]
}

export interface Series {
  ulid: string
  title: string
  mediaType: MediaType
  count: number
}

export interface SeriesList {
  items: Series[]
}

export interface ChannelSeries {
  ulid: string
  title: string
  mediaType: MediaType
  count: number
  mediaUlid: string
  image: string
}

export interface ChannelSeriesList {
  items: ChannelSeries[]
}

export interface SeriesItem {
  ulid: string
  title: string
  publish: boolean
}

export interface SeriesDetail {
  ulid: string
  title: string
  mediaType: MediaType
  channelUlid: string
  items: SeriesItem[]
  candidates: SeriesItem[]
}

export interface SeriesCreateOut {
  ulid: string
}
