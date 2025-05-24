import CryptoJS from 'crypto-js'

const SECRET_KEY = CryptoJS.enc.Utf8.parse(String(process.env.NEXT_PUBLIC_ENCRYPT_KEY))
const IV = CryptoJS.enc.Utf8.parse(String(process.env.NEXT_PUBLIC_ENCRYPT_IV))

export const encrypt = (plainText: string): string => {
  if (!plainText) return ''
  const encrypted = CryptoJS.AES.encrypt(plainText, SECRET_KEY, {
    iv: IV,
    mode: CryptoJS.mode.CBC,
    padding: CryptoJS.pad.Pkcs7,
  })
  return encrypted.toString()
}
