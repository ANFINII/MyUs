import { createRouter } from '@tanstack/react-router'
import { AppProvider } from 'components/provider/AppProvider'
import Custom404 from 'components/widgets/Status/Custom404'
import Custom500 from 'components/widgets/Status/Custom500'
import { routeTree } from '../routeTree.gen'

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

export const router = createRouter({
  routeTree,
  parseSearch,
  stringifySearch,
  InnerWrap: AppProvider,
  defaultNotFoundComponent: Custom404,
  defaultErrorComponent: Custom500,
})

declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
}
