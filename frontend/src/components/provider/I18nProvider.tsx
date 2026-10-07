import { useMemo } from 'react'
import { I18nextProvider } from 'react-i18next'
import { useLocation } from '@tanstack/react-router'
import { createI18n, DEFAULT_LOCALE, getLocale } from 'lib/i18n'

interface Props {
  children: React.ReactNode
}

export function I18nProvider(props: Props): React.JSX.Element {
  const { children } = props

  const locale = useLocation({ select: (l) => getLocale(l.publicHref) }) ?? DEFAULT_LOCALE
  const i18n = useMemo(() => createI18n(locale), [locale])

  return <I18nextProvider i18n={i18n}>{children}</I18nextProvider>
}
