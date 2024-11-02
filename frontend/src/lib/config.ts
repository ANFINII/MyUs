import { Req, Query, Headers, Config } from 'types/global'

export const API_URL = process.env.NEXT_PUBLIC_API_URL
export const AUTH_NO_PATHS: string[] = ['/account/login', '/account/signup']

export const cookieHeader = (req?: Req, query?: Query, header?: Headers): Config => {
  const cookie = req?.headers.cookie || ''
  const headers = { cookie, ...(header && { ...header }) }
  const config = { headers, ...(query && { params: query }) }
  return config
}
