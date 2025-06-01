import { MediaUser } from 'types/internal/media'
import { GenderType, NotificationType } from 'utils/constants/enum'

export interface LoginIn {
  username: string
  password: string
}

export interface SignupIn {
  email: string
  username: string
  nickname: string
  password1: string
  password2: string
  fullName: string
  lastName: string
  firstName: string
  year: number
  month: number
  day: number
  gender: Gender
}

export interface UserMe {
  avatar: string
  email: string
  nickname: string
  isActive: boolean
  isStaff: boolean
}

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

export interface ProfileOut extends User {
  fullName: string
  lastName: string
  firstName: string
  year: number
  month: number
  day: number
  age: number
  gender: GenderType
  phone: string
  countryCode: string
  postalCode: string
  prefecture: string
  city: string
  street: string
  introduction: string
}

export interface ProfileIn extends ProfileOut {
  avatar?: File
}

export interface MypageOut {
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
  banner?: File
  email: string
  tagManagerId: string
  isAdvertise: boolean
  content: string
}

export interface Follow {
  avatar: string
  nickname: string
  introduction: string
  followerCount: number
  followingCount: number
}

export interface SearchTagOut {
  sequence: number
  name: string
}

export interface ContentObject {
  id: number
  title: string
  text: string
  read: number
}

export interface Notification {
  id: number
  userFrom: MediaUser
  userTo: MediaUser
  typeNo: number
  typeName: NotificationType
  contentObject: ContentObject
  isConfirmed: boolean
}

export interface NotificationOut {
  count: number
  datas: Notification[]
}

export interface UserNotification {
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

export type UserNotificationIn = UserNotification
export type UserNotificationOut = UserNotification
