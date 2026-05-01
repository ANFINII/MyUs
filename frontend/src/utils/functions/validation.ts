export const isEmpty = (value: unknown): boolean => {
  if (typeof value === 'string') return !value.trim()
  return !value
}
