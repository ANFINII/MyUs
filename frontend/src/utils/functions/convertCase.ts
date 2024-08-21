type AnyObject = { [key: string]: any }

const snakeCase = (s: string) => s.replace(/([A-Z])/g, '_$1').toLowerCase()

export const camelSnake = <T extends AnyObject>(obj: AnyObject): T => {
  const result: AnyObject = Array.isArray(obj) ? [] : {}
  Object.entries(obj).forEach(([key, value]) => {
    result[snakeCase(key)] = value
  })
  return result as T
}

const camelCase = (s: string) => s.replace(/([-_][a-z])/gi, ($1) => $1.toUpperCase().replace('-', '').replace('_', ''))

export const snakeCamel = <T extends AnyObject>(obj: AnyObject): T => {
  const result: AnyObject = Array.isArray(obj) ? [] : {}
  Object.entries(obj).forEach(([key, value]) => {
    result[camelCase(key)] = value
  })
  return result as T
}
