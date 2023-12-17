export interface User {
  id: number
  avatar: string
  email: string
  username: string
  nickname: string
  isActive: boolean
  isStaff: boolean
  lastLogin: string
  dateJoined: string
}

export interface Profile {
  id: number
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
}

export interface UserProfile extends User {
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
