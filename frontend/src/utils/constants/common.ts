export const isEmpty = (obj: unknown): boolean => {
  if (obj === undefined || obj === null) return true
  return Object.keys(obj).length === 0
}
