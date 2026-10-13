import { useCallback, useEffect, useRef, useState } from 'react'

const getRecognitionClass = (): (new () => Recognition) | undefined => {
  const speechWindow = window as unknown as Record<string, (new () => Recognition) | undefined>
  return speechWindow.SpeechRecognition ?? speechWindow.webkitSpeechRecognition
}

interface RecognitionItem {
  transcript: string
  isFinal: boolean
}

interface RecognitionResult {
  item: (j: number) => RecognitionItem
  isFinal: boolean
}

interface RecognitionEvent {
  results: { item: (i: number) => RecognitionResult; length: number }
  resultIndex: number
}

interface Recognition {
  continuous: boolean
  interimResults: boolean
  lang: string
  start: () => void
  stop: () => void
  onresult: ((event: RecognitionEvent) => void) | null
  onend: (() => void) | null
  onerror: (() => void) | null
}

interface OutProps {
  isRecording: boolean
  isSpeaking: boolean
  isSupported: boolean
  handleToggle: () => void
}

interface Props {
  onResult: (transcript: string) => void
  lang?: string
}

export function useRecording(props: Props): OutProps {
  const { onResult, lang = 'ja-JP' } = props

  const onResultRef = useRef<(transcript: string) => void>(onResult)
  const recognitionRef = useRef<Recognition | null>(null)
  const speakingTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const [isRecording, setIsRecording] = useState<boolean>(false)
  const [isSpeaking, setIsSpeaking] = useState<boolean>(false)
  const isSupported = getRecognitionClass() !== undefined

  onResultRef.current = onResult

  const clearSpeakingTimer = (): void => {
    if (speakingTimerRef.current) clearTimeout(speakingTimerRef.current)
    speakingTimerRef.current = null
  }

  useEffect(() => {
    return () => {
      recognitionRef.current?.stop()
      if (speakingTimerRef.current) clearTimeout(speakingTimerRef.current)
    }
  }, [])

  const handleToggle = useCallback((): void => {
    if (isRecording) {
      recognitionRef.current?.stop()
      setIsRecording(false)
      return
    }

    const RecognitionClass = getRecognitionClass()
    if (!RecognitionClass) return

    const recognition = new RecognitionClass()
    recognition.continuous = true
    recognition.interimResults = true
    recognition.lang = lang

    recognition.onresult = (event) => {
      const { results, resultIndex } = event
      for (let i = resultIndex; i < results.length; i++) {
        const result = results.item(i)
        clearSpeakingTimer()
        if (result.isFinal) {
          onResultRef.current(result.item(0).transcript)
          setIsSpeaking(false)
        } else {
          setIsSpeaking(true)
          speakingTimerRef.current = setTimeout(() => setIsSpeaking(false), 500)
        }
      }
    }

    recognition.onend = () => {
      setIsRecording(false)
      setIsSpeaking(false)
    }
    recognition.onerror = () => {
      setIsRecording(false)
      setIsSpeaking(false)
    }
    recognitionRef.current = recognition
    recognition.start()
    setIsRecording(true)
  }, [isRecording, lang])

  return { isRecording, isSpeaking, isSupported, handleToggle }
}
