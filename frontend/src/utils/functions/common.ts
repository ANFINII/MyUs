import { ParsedUrlQuery } from 'querystring'

export const PAGE_SIZE = 50

export const isActive = (isbool: boolean) => (isbool ? 'active' : '')

export const searchParams = (query: ParsedUrlQuery): { search?: string } => ({
  search: typeof query.search === 'string' && query.search ? query.search : undefined,
})

export const pageParams = (query: ParsedUrlQuery): { search?: string; limit: number; offset: number; page: number } => {
  const search = typeof query.search === 'string' && query.search ? query.search : undefined
  const raw = typeof query.page === 'string' ? Number(query.page) : 1
  const page = Number.isInteger(raw) && raw > 0 ? raw : 1
  return { search, limit: PAGE_SIZE, offset: (page - 1) * PAGE_SIZE, page }
}

export const capitalize = (str: string): string => {
  if (!str) return str
  return str.charAt(0).toUpperCase() + str.slice(1)
}

export const assertNever = (value: never): never => {
  throw new Error(`Unexpected value: ${value}`)
}

export const assertUnexpected = (value: unknown): never => {
  throw new Error(`Unexpected value: ${value}`)
}
