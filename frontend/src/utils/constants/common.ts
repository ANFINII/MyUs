export const isEmpty = (obj?: Record<string, any>): boolean => {
  return obj === undefined || Object.keys(obj).length === 0
}
