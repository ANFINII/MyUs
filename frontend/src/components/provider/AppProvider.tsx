import { I18nProvider } from 'components/provider/I18nProvider'
import { QueryProvider } from 'components/provider/QueryProvider'
import { ToastProvider } from 'components/provider/ToastProvider'
import { UserProvider } from 'components/provider/UserProvider'

interface Props {
  children: React.ReactNode
}

export function AppProvider(props: Props): React.JSX.Element {
  const { children } = props

  return (
    <I18nProvider>
      <QueryProvider>
        <UserProvider>
          <ToastProvider>{children}</ToastProvider>
        </UserProvider>
      </QueryProvider>
    </I18nProvider>
  )
}
