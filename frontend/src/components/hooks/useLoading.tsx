import { useState } from 'react'

interface OutProps {
  loading: boolean
  handleLoading: (loading: boolean) => void
}

export function useLoading(): OutProps {
  const [loading, setLoading] = useState<boolean>(false)
  const handleLoading = (loading: boolean) => setLoading(loading)
  return { loading, handleLoading }
}
