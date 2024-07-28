import { useState } from 'react'

interface OutProps {
  toastContent: string
  isError: boolean
  isToast: boolean
  setIsToast: React.Dispatch<React.SetStateAction<boolean>>
  handleToast: (content: string, isError: boolean) => void
}

export const useToast = (): OutProps => {
  const [isError, setIsError] = useState<boolean>(false)
  const [isToast, setIsToast] = useState<boolean>(false)
  const [toastContent, setToastContent] = useState<string>('')

  const handleToast = (content: string, isError: boolean): void => {
    setToastContent(content)
    setIsError(isError)
    setIsToast(true)
  }

  return { toastContent, isError, isToast, setIsToast, handleToast }
}
