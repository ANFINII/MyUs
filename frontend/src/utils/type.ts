export interface ProfileResponse {
  avatar: string
  email: string
  username: string
  nickname: string
  fullname: string
  lastname: string
  firstname: string
  year: number
  month: number
  day: number
  age: number
  gender: string
  phone: string
  country_code: string
  postal_code: string
  prefecture: string
  city: string
  address: string
  building: string
  introduction: string
  [key: number]: number
}

export interface MypageResponse {
  banner: string
  nickname: string
  email: string
  follower_num: number
  following_num: number
  plan: string
  plan_date: string
  is_advertise: boolean
  content: string
}

export interface author {
  id: number
  nickname: string
  image: string
}

export interface Query {
  name: string
  count: number
}

export interface MediaResponse {
  id: number
  title: string
  content: string
  like: number
  read: number
  comment_num: number
  publish: boolean
  created: string
  updated: string
  author: author
  model_name: string
}

export interface VideoResponse extends MediaResponse {
  image: string
  video: string
  convert: string
}

export interface MusicResponse extends MediaResponse {
  music: string
  lyric: string
  download: boolean
}

export interface ImageResponse extends MediaResponse {
  image: string
}

export interface ChatResponse extends MediaResponse {
  read: number
  joined: number
  thread: number
}

export interface FollowResponse {
  id: number
  title: string
  content: string
  introduction: string
  like: number
  read: number
  comment_num: number
  publish: boolean
  created: string
  mypage: MypageResponse
  author: author
}
