export const isEmpty = (value: unknown): boolean => {
  if (typeof value === 'string') return !value.trim()
  return !value
}

export const isHttpsUrl = (value: string): boolean => {
  try {
    const url = new URL(value)
    return url.protocol === 'https:'
  } catch {
    return false
  }
}
