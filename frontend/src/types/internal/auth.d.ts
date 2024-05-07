import { Gender } from 'utils/constants/enum'

export interface User {
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
  street: string
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
  gender: Gender
  phone: string
  countryCode: string
  postalCode: string
  prefecture: string
  city: string
  street: string
  building: string
  introduction: string
}

export interface Mypage {
  banner: string
  nickname: string
  email: string
  followerCount: number
  followingCount: number
  tagManagerId: string
  plan: string
  planDate: string
  isAdvertise: boolean
  content: string
}

export interface MypageIn {
  banner: string
  email: string
  tagManagerId: string
  isAdvertise: boolean
  content: string
}

export interface NotificationIn {
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

export type NotificationOut = NotificationIn

export interface LoginRequest {
  username: string
  password: string
}
