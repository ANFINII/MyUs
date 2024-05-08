export const isEmpty = (obj: Record<string, any>): boolean => {
  return obj === undefined || obj === null || Object.keys(obj).length === 0
}
