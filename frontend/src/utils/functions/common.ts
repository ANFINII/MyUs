import { ParsedUrlQuery } from 'querystring'

export const isActive = (isbool: boolean) => (isbool ? 'active' : '')

export const searchParams = (query: ParsedUrlQuery): { search?: string } => ({
  search: typeof query.search === 'string' && query.search ? query.search : undefined,
})

export const capitalize = (str: string): string => {
  if (!str) return str
  return str.charAt(0).toUpperCase() + str.slice(1)
}
