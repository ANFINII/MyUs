import { useMemo } from 'react'
import { ParsedUrlQuery, ParsedUrlQueryInput } from 'querystring'
import { useRouter as useTanstackRouter, useRouterState } from '@tanstack/react-router'
import { getLocale } from 'lib/i18n'

type Url = string | { pathname: string; query?: ParsedUrlQueryInput }

export interface Router {
  pathname: string
  query: ParsedUrlQuery
  locale?: string
  push: (url: Url) => Promise<boolean>
  replace: (url: Url) => Promise<boolean>
  buildUrl: (href: string) => string
  canBack: () => boolean
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

export function useRouter(): Router {
  const router = useTanstackRouter()
  const location = useRouterState({ select: (s) => s.location })
  const params = useRouterState({ select: (s) => s.matches.at(-1)?.params })

  return useMemo(() => {
    const pathname = location.pathname
    const locale = getLocale(location.publicHref)
    const pathParams: Record<string, string> = {}
    Object.entries(params ?? {}).forEach(([key, value]) => {
      if (typeof value === 'string') pathParams[key] = value
    })
    const query: ParsedUrlQuery = { ...(location.search as ParsedUrlQuery), ...pathParams }

    const toHref = (url: Url): string => {
      if (typeof url !== 'string') return `${url.pathname}${toSearch(url.query ?? {})}`
      if (url.startsWith('?')) return `${location.pathname}${url}`
      return url
    }

    const navigate = async (url: Url, replace: boolean): Promise<boolean> => {
      if (typeof url === 'string' && /^https?:\/\//.test(url)) {
        if (replace) window.location.replace(url)
        else window.location.assign(url)
        return true
      }
      await router.navigate({ href: toHref(url), replace })
      return true
    }

    return {
      pathname,
      query,
      locale,
      push: (url) => navigate(url, false),
      replace: (url) => navigate(url, true),
      buildUrl: (href) => `${window.location.origin}${locale ? `/${locale}` : ''}${href}`,
      canBack: () => window.history.length > 1,
      back: () => router.history.back(),
      reload: () => window.location.reload(),
    }
  }, [router, location, params])
}
