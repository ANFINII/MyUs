import { useState } from 'react'

interface OutProps {
  error?: string
  validate: (values: Record<string, unknown>) => boolean
}

export const useRequired = (): OutProps => {
  const [error, setError] = useState<string | undefined>(undefined)

  const validate = (values: Record<string, unknown>): boolean => {
    const isFalsy = Object.values(values).some((value) => !value)
    setError(isFalsy ? '' : undefined)
    return !isFalsy
  }

  return { error, validate }
}
