import { useMemo } from 'react'
import { I18nextProvider } from 'react-i18next'
import { createI18n, DEFAULT_LOCALE } from 'lib/i18n'
import { useRouter } from 'components/hooks/useRouter'

interface Props {
  children: React.ReactNode
}

export function I18nProvider(props: Props): React.JSX.Element {
  const { children } = props

  const router = useRouter()
  const locale = router.locale ?? DEFAULT_LOCALE
  const i18n = useMemo(() => createI18n(locale), [locale])

  return <I18nextProvider i18n={i18n}>{children}</I18nextProvider>
}
