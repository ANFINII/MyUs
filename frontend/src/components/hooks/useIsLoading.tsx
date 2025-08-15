import { useState } from 'react'

interface OutProps {
  isLoading: boolean
  handleLoading: (isLoading: boolean) => void
}

export function useIsLoading(): OutProps {
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const handleLoading = (isLoading: boolean) => setIsLoading(isLoading)
  return { isLoading, handleLoading }
}
