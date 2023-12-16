type AnyObject = { [key: string]: any }

const snakeCase = (s: string) => s.replace(/([A-Z])/g, '_$1').toLowerCase()

const transformValue = (value: any) => {
  if (typeof value === 'object' && value !== null) {
    return camelSnake(value)
  }
  return value
}

export const camelSnake = <T extends AnyObject>(obj: AnyObject): T => {
  const result: AnyObject = Array.isArray(obj) ? [] : {}
  Object.entries(obj).forEach(([key, value]) => {
    result[snakeCase(key)] = transformValue(value)
  })
  return result as T
}

export const convertObjectKeys = <T extends AnyObject>(obj: AnyObject, convertKey: (key: string) => string): T =>
  Object.entries(obj).reduce((result, [key, value]) => {
    const transformedValue = typeof value === 'object' && value !== null ? convertObjectKeys(value, convertKey) : value
    return Object.assign(result, { [convertKey(key)]: transformedValue })
  }, {} as T)

const camelCase = (s: string): string => {
  return s.replace(/([-_][a-z])/gi, ($1) => $1.toUpperCase().replace('-', '').replace('_', ''))
}

export const snakeCamel = <T extends AnyObject>(obj: AnyObject): T => convertObjectKeys(obj, camelCase)
