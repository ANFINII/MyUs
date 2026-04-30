export interface AdvertiseIn {
  title: string
  url: string
  content: string
  publish: boolean
  period: string | null
  image?: File
  video?: File
}

export interface AdvertiseUpdateIn {
  title: string
  url: string
  content: string
  publish: boolean
  period: string | null
  image?: File
  video?: File
}

export interface Advertise {
  ulid: string
  title: string
  url: string
  content: string
  image: string
  video: string
  read: number
  type: string
  period: string | null
  publish: boolean
  created: Date
  updated: Date
}

export interface AdvertiseList {
  datas: Advertise[]
  total: number
}

export interface AdvertiseSearchParams {
  search?: string
  limit?: number
  offset?: number
}
