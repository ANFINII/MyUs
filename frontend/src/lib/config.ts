import { Req, Query, Config } from 'types/global'

export const API_URL = process.env.NEXT_PUBLIC_API_URL as string
export const AUTH_NO_PATHS: string[] = ['/account/login', '/account/signup']

export const cookieHeader = (req?: Req, query?: Query): Config => {
  const cookie = req?.headers.cookie
  const headers = { cookie }
  const config = { headers, ...(query && { params: query }) }
  return config
}
