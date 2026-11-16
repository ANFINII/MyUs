import { I18nProvider } from 'components/provider/I18nProvider'
import { MusicPlayerProvider } from 'components/provider/MusicPlayerProvider'
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
        <UserProvider>
          <MusicPlayerProvider>{children}</MusicPlayerProvider>
        </UserProvider>
      </QueryProvider>
    </I18nProvider>
  )
}
