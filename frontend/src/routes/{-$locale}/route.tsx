import { createFileRoute, notFound, Outlet } from '@tanstack/react-router'
import { LOCALES } from 'lib/i18n'

export const Route = createFileRoute('/{-$locale}')({
  beforeLoad: ({ params }) => {
    if (params.locale !== undefined && !LOCALES.includes(params.locale)) throw notFound()
  },
  component: Outlet,
})
