import { cbc } from '@noble/ciphers/aes.js'

const encoder = new TextEncoder()
const SECRET_KEY = encoder.encode(String(process.env.NEXT_PUBLIC_ENCRYPT_KEY))
const IV = encoder.encode(String(process.env.NEXT_PUBLIC_ENCRYPT_IV))

export const encrypt = (plainText: string): string => {
  if (!plainText) return ''
  const encrypted = cbc(SECRET_KEY, IV).encrypt(encoder.encode(plainText))
  return btoa(String.fromCharCode(...encrypted))
}
