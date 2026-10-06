import { useMemo } from 'react'
import { ParsedUrlQuery, ParsedUrlQueryInput } from 'querystring'
import { useRouter, useRouterState } from '@tanstack/react-router'
import { LOCALES } from 'lib/i18n'

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

const toSearch = (query: ParsedUrlQueryInput): string => {
  const params = new URLSearchParams()
  Object.entries(query).forEach(([key, value]) => {
    if (value === undefined || value === null) return
    if (Array.isArray(value)) value.forEach((v) => params.append(key, String(v)))
    else params.append(key, String(value))
  })
  const search = params.toString()
  return search ? `?${search}` : ''
}

export function useAppRouter(): AppRouter {
  const router = useRouter()
  const location = useRouterState({ select: (s) => s.location })
  const params = useRouterState({ select: (s) => s.matches.at(-1)?.params })

  return useMemo(() => {
    const first = location.pathname.split('/')[1] ?? ''
    const locale = LOCALES.includes(first) ? first : undefined
    const prefix = locale ? `/${locale}` : ''
    const pathname = location.pathname.slice(prefix.length) || '/'
    const pathParams: Record<string, string> = {}
    Object.entries(params ?? {}).forEach(([key, value]) => {
      if (key !== 'locale' && typeof value === 'string') pathParams[key] = value
    })
    const query: ParsedUrlQuery = { ...(location.search as ParsedUrlQuery), ...pathParams }

    const toHref = (url: Url): string => {
      if (typeof url !== 'string') return `${prefix}${url.pathname}${toSearch(url.query ?? {})}`
      if (url.startsWith('?')) return `${location.pathname}${url}`
      return `${prefix}${url}`
    }

    const navigate = async (url: Url, replace: boolean): Promise<boolean> => {
      if (typeof url === 'string' && /^https?:\/\//.test(url)) {
        window.location.assign(url)
        return true
      }
      await router.navigate({ href: toHref(url), replace })
      return true
    }

    return {
      pathname,
      query,
      isReady: true,
      locale,
      push: (url) => navigate(url, false),
      replace: (url) => navigate(url, true),
      back: () => router.history.back(),
      reload: () => window.location.reload(),
    }
  }, [router, location, params])
}
