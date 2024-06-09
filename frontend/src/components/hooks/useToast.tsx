import { useState, useCallback, useEffect } from 'react'
import { useRouter } from 'next/router'

interface OutProps {
  toastContent: string
  isError: boolean
  isToast: boolean
  setIsToast: React.Dispatch<React.SetStateAction<boolean>>
  toastFunc: (content: string, isError: boolean) => void
}

export const useToast = (): OutProps => {
  const router = useRouter()
  const [toastContent, setToastContent] = useState<string>('')
  const [isError, setIsError] = useState<boolean>(false)
  const [isToast, setIsToast] = useState<boolean>(false)

  const toastFunc = useCallback((content: string, isError: boolean): void => {
    setToastContent(content)
    setIsError(isError)
    setIsToast(true)
  }, [])

  useEffect(() => {
    const toastContent = router.query.toastContent as string
    if (toastContent) {
      toastFunc(toastContent, false)
    }
  }, [router.query, toastFunc])

  return { toastContent, isError, isToast, setIsToast, toastFunc }
}
