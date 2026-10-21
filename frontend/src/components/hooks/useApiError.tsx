import { Dispatch, SetStateAction, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { isTranslationKey } from 'lib/i18n'

interface OutProps {
  message: string
  setMessage: Dispatch<SetStateAction<string>>
  handleError: (content: string, errorMessage?: string) => void
}

interface Props {
  handleToast: (content: string, isError: boolean) => void
}

export function useApiError(props: Props): OutProps {
  const { handleToast } = props

  const { t, i18n } = useTranslation()
  const [message, setMessage] = useState<string>('')

  const handleError = (content: string, errorMessage?: string): void => {
    if (errorMessage) {
      setMessage(isTranslationKey(i18n, errorMessage) ? t(errorMessage) : errorMessage)
    } else {
      handleToast(content, true)
    }
  }
  return { message, setMessage, handleError }
}
