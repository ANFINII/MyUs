import { I18nProvider } from 'components/provider/I18nProvider'
import { QueryProvider } from 'components/provider/QueryProvider'
import { UserProvider } from 'components/provider/UserProvider'

interface Props {
  children: React.ReactNode
}

export function AppProvider(props: Props): React.JSX.Element {
  const { children } = props

  return (
    <I18nProvider>
      <QueryProvider>
        <UserProvider>{children}</UserProvider>
      </QueryProvider>
    </I18nProvider>
  )
}
