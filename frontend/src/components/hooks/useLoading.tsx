import { useState } from 'react'

interface OutProps {
  isLoading: boolean
  handleLoading: (isLoading: boolean) => void
}

export function useLoading(): OutProps {
  const [isLoading, setIsLoading] = useState<boolean>(false)
  return { isLoading, handleLoading: setIsLoading }
}
