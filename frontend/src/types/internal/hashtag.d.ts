import { MediaType } from 'utils/constants/enum'

export interface HashtagItem {
  ulid: string
  name: string
}

export interface HashtagOut {
  ulid: string
  name: string
}

export interface MediaHashtagsUpdateIn {
  mediaType: MediaType
  mediaUlid: string
  hashtags: HashtagItem[]
}
