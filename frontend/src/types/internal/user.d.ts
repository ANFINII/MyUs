import { NotificationUser } from 'types/internal/media'
import { GenderType, MediaType, NotificationType } from 'utils/constants/enum'

export interface UserMe {
  avatar: string
  ulid: string
  nickname: string
  isActive: boolean
  isStaff: boolean
}

export interface User {
  avatar: string
  ulid: string
  email: string
  username: string
  nickname: string
  isActive: boolean
  isStaff: boolean
  lastLogin: string
  dateJoined: string
}

export interface ProfileOut extends User {
  lastName: string
  firstName: string
  year: number
  month: number
  day: number
  gender: GenderType
  phone: string
  countryCode: string
  postalCode: string
  prefecture: string
  city: string
  street: string
  introduction: string
}

export interface ProfileIn {
  avatarFile?: File
  email: string
  username: string
  nickname: string
  lastName: string
  firstName: string
  gender: GenderType
  year: number
  month: number
  day: number
  phone: string
  countryCode: string
  postalCode: string
  prefecture: string
  city: string
  street: string
  introduction: string
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
  bannerFile?: File
  email: string
  tagManagerId: string
  isAdvertise: boolean
  content: string
}

export interface Follow {
  avatar: string
  ulid: string
  nickname: string
  introduction: string
  followerCount: number
  followingCount: number
}

export interface FollowIn {
  ulid: string
  isFollow: boolean
}

export interface FollowOut {
  isFollow: boolean
  followerCount: number
}

export interface LikeMediaIn {
  ulid: string
  mediaType: MediaType
}

export interface LikeCommentIn {
  ulid: string
}

export interface LikeOut {
  isLike: boolean
  likeCount: number
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
  userFrom: NotificationUser
  userTo: NotificationUser
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
