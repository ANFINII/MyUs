import { Dispatch, SetStateAction, useState } from 'react'

interface OutProps {
  message: string
  setMessage: Dispatch<SetStateAction<string>>
  handleError: (content: string, errorMessage?: string) => void
}

interface Props {
  handleToast: (content: string, isError: boolean) => void
}

export const useApiError = (props: Props): OutProps => {
  const { handleToast } = props

  const [message, setMessage] = useState<string>('')

  const handleError = (content: string, errorMessage?: string) => {
    if (errorMessage) {
      setMessage(errorMessage)
    } else {
      handleToast(content, true)
    }
  }
  return { message, setMessage, handleError }
}
