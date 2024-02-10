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

const camelase = (s: string) => s.replace(/([-_][a-z])/gi, ($1) => $1.toUpperCase().replace('-', '').replace('_', ''))

export const snakeCamel = <T extends AnyObject>(obj: AnyObject): T => {
  const result: AnyObject = Array.isArray(obj) ? [] : {}
  for (const key in obj) {
    if (Object.prototype.hasOwnProperty.call(obj, key)) {
      let value = obj[key]
      if (typeof value === 'object' && value !== null) {
        value = snakeCamel(value)
      }
      result[camelase(key)] = value
    }
  }
  return result as T
}
