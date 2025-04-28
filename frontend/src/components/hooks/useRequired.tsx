import { useState } from 'react'

interface OutProps {
  isRequired: boolean
  isRequiredCheck: (values: Record<string, unknown>) => boolean
}

export const useRequired = (): OutProps => {
  const [isRequired, setIsRequired] = useState(false)

  const isRequiredCheck = (values: Record<string, unknown>): boolean => {
    const isFalsy = Object.values(values).some((value) => !value)
    setIsRequired(isFalsy)
    return !isFalsy
  }

  return { isRequired, isRequiredCheck }
}
