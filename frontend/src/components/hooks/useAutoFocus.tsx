import { useRef, useEffect } from 'react'

export default function useAutoFocus() {
  const inputRef = useRef<HTMLInputElement>(null)
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus()
    }
  }, [])
  return inputRef
}
