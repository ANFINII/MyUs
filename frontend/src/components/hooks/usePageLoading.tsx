import { useRouterState } from '@tanstack/react-router'

interface OutProps {
  loading: boolean
}

export function usePageLoading(): OutProps {
  const loading = useRouterState({ select: (s) => s.status === 'pending' })
  return { loading }
}
