import { Req, Query, Config } from 'types/global'

export const API_URL = process.env.NEXT_PUBLIC_API_URL
export const AUTH_NO_PATHS: string[] = ['/account/login', '/account/signup']

export const cookieHeader = (req?: Req, query?: Query): Config | undefined => {
  const cookie = req?.headers.cookie
  if (!cookie) return undefined
  const headers = { cookie }
  const config = { headers, ...(query && { params: query }) }
  return config
}
