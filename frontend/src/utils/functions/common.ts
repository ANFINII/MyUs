import { ParsedUrlQuery } from 'querystring'
import { MediaHome } from 'types/internal/media/output'
import { HomeSort } from 'utils/constants/enum'

export const PAGE_SIZE = 50

export const isActive = (isbool: boolean) => (isbool ? 'active' : '')

export const searchParams = (query: ParsedUrlQuery): { search?: string } => ({
  search: typeof query.search === 'string' && query.search ? query.search : undefined,
})

export const homeParams = (query: ParsedUrlQuery): { search?: string; sort: HomeSort } => {
  const sort = Object.values(HomeSort).find((value) => value === query.sort) ?? HomeSort.Recommend
  return { ...searchParams(query), sort }
}

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

export const assertUnexpected = (value: unknown): never => {
  throw new Error(`Unexpected value: ${value}`)
}

export const shuffleItems = <T>(items: T[]): T[] => {
  const ret = [...items]
  for (let i = ret.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    const tmp = ret[i] as T
    ret[i] = ret[j] as T
    ret[j] = tmp
  }
  return ret
}

export const mediaCount = (media: MediaHome): number => {
  const { videos, musics, blogs, comics, pictures, chats } = media
  return videos.length + musics.length + blogs.length + comics.length + pictures.length + chats.length
}

export const pathMediaName = (pathname: string): string => capitalize(pathname.split('/')[2] ?? '')
