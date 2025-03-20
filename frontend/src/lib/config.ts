import { AxiosError } from 'axios'
import { Req, Config } from 'types/global'

export const API_URL = String(process.env.NEXT_PUBLIC_API_URL)
export const AUTH_NO_PATHS = ['/account/login', '/account/signup']

export const cookieHeader = <T>(req?: Req, query?: T): Config => {
  const cookie = req?.headers.cookie
  const headers = { cookie }
  const config = { headers, ...(query && { params: query }) }
  return config
}

export const AxiosErrorLog = (e: AxiosError) => {
  const errResponse = e.response
  const errRequest = e.request

  console.group()
  console.log('%c========== Axios Error Start ==========', 'color: red;')
  console.log('Status:', errResponse?.status)
  console.log('Message:', errResponse?.statusText)
  console.log('Path:', errRequest?.path)
  console.log('Header:', errRequest?._header)
  console.log('========== Axios Error End ==========')
  console.groupEnd()
}
