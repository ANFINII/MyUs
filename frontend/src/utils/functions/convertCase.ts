type AnyObject = { [key: string]: any }

const snakeCase = (s: string) => s.replace(/([A-Z])/g, '_$1').toLowerCase()

export const camelSnake = <T extends AnyObject>(obj: AnyObject): T => {
  const transformValue = (value: any) => {
    if (value instanceof File) {
      return value
    } else if (typeof value === 'object' && value !== null) {
      return camelSnake(value)
    }
    return value
  }
  const result: AnyObject = Array.isArray(obj) ? [] : {}
  Object.entries(obj).forEach(([key, value]) => {
    result[snakeCase(key)] = transformValue(value)
  })
  return result as T
}

const camelCase = (s: string) => s.replace(/([-_][a-z])/gi, ($1) => $1.toUpperCase().replace('-', '').replace('_', ''))

export const snakeCamel = <T extends AnyObject>(obj: AnyObject): T => {
  const transformValue = (value: any) => {
    if (typeof value === 'object' && value !== null) {
      return snakeCamel(value)
    }
    return value
  }
  const result: AnyObject = Array.isArray(obj) ? [] : {}
  Object.entries(obj).forEach(([key, value]) => {
    result[camelCase(key)] = transformValue(value)
  })
  return result as T
}
