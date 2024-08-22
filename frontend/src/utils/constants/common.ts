import { AnyObject } from 'types/internal/other'

export const isEmpty = (obj: AnyObject): boolean => {
  return obj === undefined || obj === null || Object.keys(obj).length === 0
}
