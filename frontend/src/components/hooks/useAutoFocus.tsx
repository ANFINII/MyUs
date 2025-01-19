import { useRef, useEffect, RefObject } from 'react'

export default function useAutoFocus(): RefObject<HTMLInputElement> {
  const inputRef = useRef<HTMLInputElement>(null)
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus()
    }
  }, [])
  return inputRef
}
