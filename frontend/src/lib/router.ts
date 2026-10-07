import { createRouter, LocationRewrite } from '@tanstack/react-router'
import { getLocale } from 'lib/i18n'
import { routeTree } from 'lib/routes'
import { AppProvider } from 'components/provider/AppProvider'
import Custom404 from 'components/widgets/Status/Custom404'
import Custom500 from 'components/widgets/Status/Custom500'

const parseSearch = (search: string): Record<string, string> => Object.fromEntries(new URLSearchParams(search))

const stringifySearch = (search: Record<string, unknown>): string => {
  const params = new URLSearchParams()
  Object.entries(search).forEach(([key, value]) => {
    if (value === undefined || value === null) return
    if (Array.isArray(value)) value.forEach((v) => params.append(key, String(v)))
    else params.append(key, String(value))
  })
  const query = params.toString()
  return query ? `?${query}` : ''
}

const rewrite: LocationRewrite = {
  input: ({ url }) => {
    const locale = getLocale(url.pathname)
    if (!locale) return undefined
    url.pathname = url.pathname.slice(locale.length + 1) || '/'
    return url
  },
  output: ({ url }) => {
    const locale = getLocale(window.location.pathname)
    if (!locale) return undefined
    url.pathname = url.pathname === '/' ? `/${locale}` : `/${locale}${url.pathname}`
    return url
  },
}

export const router = createRouter({
  routeTree,
  parseSearch,
  stringifySearch,
  rewrite,
  InnerWrap: AppProvider,
  defaultNotFoundComponent: Custom404,
  defaultErrorComponent: Custom500,
})

declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
}
