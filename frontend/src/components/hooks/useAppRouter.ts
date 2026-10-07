import { useMemo } from 'react'
import { ParsedUrlQueryInput } from 'querystring'
import { useRouter, useRouterState } from '@tanstack/react-router'
import { getLocale } from 'lib/i18n'

type Url = string | { pathname: string; query?: ParsedUrlQueryInput }

export interface AppRouter {
  pathname: string
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

  return useMemo(() => {
    const pathname = location.pathname
    const locale = getLocale(location.publicHref)

    const toHref = (url: Url): string => {
      if (typeof url !== 'string') return `${url.pathname}${toSearch(url.query ?? {})}`
      if (url.startsWith('?')) return `${location.pathname}${url}`
      return url
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
      locale,
      push: (url) => navigate(url, false),
      replace: (url) => navigate(url, true),
      back: () => router.history.back(),
      reload: () => window.location.reload(),
    }
  }, [router, location])
}
