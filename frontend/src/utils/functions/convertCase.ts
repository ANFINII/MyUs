const snakeCase = (s: string) => s.replace(/([A-Z])/g, '_$1').toLowerCase()
const camelCase = (s: string) => s.replace(/([-_][a-z])/gi, ($1) => $1.toUpperCase().replace('-', '').replace('_', ''))

const convertKeys = (value: unknown, convert: (key: string) => string): unknown => {
  if (Array.isArray(value)) return value.map((v) => convertKeys(v, convert))
  if (value === null || typeof value !== 'object' || value instanceof File) return value
  return Object.fromEntries(Object.entries(value).map(([key, v]) => [convert(key), convertKeys(v, convert)]))
}

export const camelSnake = (obj: object): unknown => convertKeys(obj, snakeCase)

export const snakeCamel = (obj: unknown): unknown => convertKeys(obj, camelCase)
