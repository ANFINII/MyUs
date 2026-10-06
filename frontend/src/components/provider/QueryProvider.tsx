import { useState } from 'react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { createQueryClient } from 'lib/query/client'

interface Props {
  children: React.ReactNode
}

export function QueryProvider(props: Props): React.JSX.Element {
  const { children } = props

  const [client] = useState<QueryClient>(createQueryClient)

  return <QueryClientProvider client={client}>{children}</QueryClientProvider>
}
