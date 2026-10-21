import { useRef, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { isTranslationKey } from 'lib/i18n'
import { ToastType } from 'types/internal/other'

interface OutProps {
  toast: ToastType
  handleToast: (content: string, isError: boolean) => void
}

export function useToast(): OutProps {
  const { t, i18n } = useTranslation()
  const [content, setContent] = useState<string>('')
  const [isError, setIsError] = useState<boolean>(false)
  const [isToast, setIsToast] = useState<boolean>(false)
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null)

  const toast = { content, isError, isToast, setIsToast }

  const handleToast = (content: string, isError: boolean): void => {
    setContent(isTranslationKey(i18n, content) ? t(content) : content)
    setIsError(isError)
    setIsToast(true)
    if (timerRef.current) clearTimeout(timerRef.current)
    timerRef.current = setTimeout(() => setIsToast(false), 5000)
  }

  return { toast, handleToast }
}
