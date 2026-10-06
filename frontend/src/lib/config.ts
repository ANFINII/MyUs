import { AxiosError } from 'axios'

export const ENV = String(import.meta.env.VITE_ENV)
export const API_URL = String(import.meta.env.VITE_API_URL)
export const ENCRYPT_KEY = String(import.meta.env.VITE_ENCRYPT_KEY)
export const ENCRYPT_IV = String(import.meta.env.VITE_ENCRYPT_IV)

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
