export interface Profile {
  id: number
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
  countryCode: string
  postalCode: string
  prefecture: string
  city: string
  address: string
  building: string
  introduction: string
  [key: number]: number
}

export interface Mypage {
  id: number
  banner: string
  nickname: string
  email: string
  followerCount: number
  followingCount: number
  plan: string
  planDate: string
  isAdvertise: boolean
  content: string
}

export interface NotificationSetting {
  id: number
  isVideo: boolean
  isMusic: boolean
  isComic: boolean
  isPicture: boolean
  isBlog: boolean
  isChat: boolean
  isFollow: boolean
  isReply: boolean
  isLike: boolean
  isViews: boolean
}

export interface User {
  id: number
  nickname: string
  image: string
  isAuth: boolean
}