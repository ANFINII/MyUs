import { Req, Config } from 'types/global'

export const API_URL = String(process.env.NEXT_PUBLIC_API_URL)
export const AUTH_NO_PATHS = ['/account/login', '/account/signup']

export const cookieHeader = <T>(req?: Req, query?: T): Config => {
  const cookie = req?.headers.cookie
  const headers = { cookie }
  const config = { headers, ...(query && { params: query }) }
  return config
}
