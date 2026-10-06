import { cbc } from '@noble/ciphers/aes.js'
import { ENCRYPT_KEY, ENCRYPT_IV } from 'lib/config'

const encoder = new TextEncoder()
const SECRET_KEY = encoder.encode(ENCRYPT_KEY)
const IV = encoder.encode(ENCRYPT_IV)

export const encrypt = (plainText: string): string => {
  if (!plainText) return ''
  const encrypted = cbc(SECRET_KEY, IV).encrypt(encoder.encode(plainText))
  return btoa(String.fromCharCode(...encrypted))
}
