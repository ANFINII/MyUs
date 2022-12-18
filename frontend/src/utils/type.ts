export type ProfileType = {
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
  key: number
  gender: string
  phone: string
  postal_code: string
  prefecture: string
  city: string
  address: string
  building: string
  introduction: string
}

export type MypageType = {
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

export type MediaType = {
  id: number | null
  title: string
  content: string
  hashtag: string
  like: string
  read: number | null
  publish: boolean
  created: string
  updated: string
  author: {
    id: number | null
    title: string
    nickname: string
    image: string
  }
  data: any
}

export type VideoType = MediaType & {
  image: string
  video: string
  convert: string
}
