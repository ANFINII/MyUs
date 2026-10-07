import { useRef, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { ToastType } from 'types/internal/other'
import { Fetch, FetchError } from 'utils/constants/enum'

const fetchKeys: string[] = [...Object.values(Fetch), ...Object.values(FetchError)]

const isFetchKey = (content: string): content is Fetch | FetchError => fetchKeys.includes(content)

interface OutProps {
  toast: ToastType
  handleToast: (content: string, isError: boolean) => void
}

export const useToast = (): OutProps => {
  const { t } = useTranslation()
  const [content, setContent] = useState<string>('')
  const [isError, setIsError] = useState<boolean>(false)
  const [isToast, setIsToast] = useState<boolean>(false)
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null)

  const toast = { content, isError, isToast, setIsToast }

  const handleToast = (content: string, isError: boolean) => {
    setContent(isFetchKey(content) ? t(content) : content)
    setIsError(isError)
    setIsToast(true)
    if (timerRef.current) clearTimeout(timerRef.current)
    timerRef.current = setTimeout(() => setIsToast(false), 5000)
  }

  return { toast, handleToast }
}
