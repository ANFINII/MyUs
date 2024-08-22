type AnyObject = { [key: string]: any }

const snakeCase = (s: string) => s.replace(/([A-Z])/g, '_$1').toLowerCase()
const camelCase = (s: string) => s.replace(/([-_][a-z])/gi, ($1) => $1.toUpperCase().replace('-', '').replace('_', ''))

export const camelSnake = <T extends AnyObject>(obj: AnyObject): T => {
  const result: AnyObject = Array.isArray(obj) ? [] : {}
  for (const key in obj) {
    if (Object.prototype.hasOwnProperty.call(obj, key)) {
      const value = obj[key]
      if (typeof window !== 'undefined') {
        result[snakeCase(key)] = value
      } else if (typeof value === 'object' && value !== null) {
        result[snakeCase(key)] = camelSnake(value)
      } else {
        result[snakeCase(key)] = value
      }
    }
  }
  return result as T
}

export const snakeCamel = <T extends AnyObject>(obj: AnyObject): T => {
  const result: AnyObject = Array.isArray(obj) ? [] : {}
  for (const key in obj) {
    if (Object.prototype.hasOwnProperty.call(obj, key)) {
      const value = obj[key]
      if (typeof value === 'object' && value !== null) {
        result[camelCase(key)] = snakeCamel(value)
      } else {
        result[camelCase(key)] = value
      }
    }
  }
  return result as T
}
