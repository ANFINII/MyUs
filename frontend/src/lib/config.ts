import { AxiosError } from 'axios'
import { Req, Config } from 'types/global'

export const ENV = String(process.env.NEXT_PUBLIC_ENV)
export const API_URL = String(process.env.NEXT_PUBLIC_API_URL)

export const cookieHeader = <T>(req?: Req, query?: T): Config => {
  const cookie = req?.headers.cookie
  const headers = { cookie }
  const config = { headers, ...(query && { params: query }) }
  return config
}

export const AxiosErrorLog = (e: AxiosError) => {
  const errResponse = e.response
  const errRequest = e.request
  if (ENV === 'http://127.0.0.1') {
    console.group()
    console.log('%c========== Axios Error Start ==========', 'color: red;')
    console.log('Status:', errResponse?.status)
    console.log('Message:', errResponse?.statusText)
    console.log('Path:', errRequest?.path)
    console.log('Header:', errRequest?._header)
    console.log('%c========== Axios Error End ==========', 'color: red;')
    console.groupEnd()
  }
}
