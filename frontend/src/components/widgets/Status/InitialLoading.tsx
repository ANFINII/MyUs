import { useRouterState } from '@tanstack/react-router'
import PageLoading from './Loading'

export default function InitialLoading(): React.JSX.Element | null {
  const isInitial = useRouterState({ select: (s) => s.resolvedLocation === undefined })

  return isInitial ? <PageLoading /> : null
}
