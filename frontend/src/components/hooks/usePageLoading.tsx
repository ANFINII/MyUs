import { useRouterState } from '@tanstack/react-router'

interface OutProps {
  isLoading: boolean
}

export function usePageLoading(): OutProps {
  const isLoading = useRouterState({ select: (s) => s.status === 'pending' })
  return { isLoading }
}
