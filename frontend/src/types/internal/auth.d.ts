import { GenderType } from 'utils/constants/enum'

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
  lastName: string
  firstName: string
  year: number
  month: number
  day: number
  gender: GenderType
}
