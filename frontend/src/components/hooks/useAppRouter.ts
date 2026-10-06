import { useRouter } from 'next/router'
import { ParsedUrlQuery, ParsedUrlQueryInput } from 'querystring'

type Url = string | { pathname: string; query?: ParsedUrlQueryInput }

export interface AppRouter {
  pathname: string
  query: ParsedUrlQuery
  isReady: boolean
  locale?: string
  push: (url: Url) => Promise<boolean>
  replace: (url: Url) => Promise<boolean>
  back: () => void
  reload: () => void
}

export function useAppRouter(): AppRouter {
  return useRouter()
}
