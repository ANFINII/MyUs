import { QueryClientProvider } from '@tanstack/react-query'
import { queryClient } from 'lib/query/client'

interface Props {
  children: React.ReactNode
}

export function QueryProvider(props: Props): React.JSX.Element {
  const { children } = props

  return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
}
