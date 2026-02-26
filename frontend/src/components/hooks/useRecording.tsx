import { useCallback, useEffect, useRef, useState } from 'react'

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

  const onResultRef = useRef(onResult)
  const recognitionRef = useRef<Recognition | null>(null)
  const speakingTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const [isRecording, setIsRecording] = useState(false)
  const [isSpeaking, setIsSpeaking] = useState(false)
  const [isSupported, setIsSupported] = useState(false)

  useEffect(() => {
    setIsSupported('SpeechRecognition' in window || 'webkitSpeechRecognition' in window)
  }, [])

  useEffect(() => {
    onResultRef.current = onResult
  }, [onResult])

  useEffect(() => {
    return () => {
      recognitionRef.current?.stop()
    }
  }, [])

  const handleToggle = useCallback(() => {
    if (isRecording) {
      recognitionRef.current?.stop()
      setIsRecording(false)
      return
    }

    const SpeechRecognitionClass =
      (window as unknown as Record<string, new () => Recognition>).SpeechRecognition ??
      (window as unknown as Record<string, new () => Recognition>).webkitSpeechRecognition

    if (!SpeechRecognitionClass) return

    const recognition = new SpeechRecognitionClass()
    recognition.continuous = true
    recognition.interimResults = true
    recognition.lang = lang

    recognition.onresult = (event) => {
      const { results, resultIndex } = event
      for (let i = resultIndex; i < results.length; i++) {
        const result = results.item(i)
        if (result.isFinal) {
          onResultRef.current(result.item(0).transcript)
          setIsSpeaking(false)
          if (speakingTimerRef.current) clearTimeout(speakingTimerRef.current)
        } else {
          setIsSpeaking(true)
          if (speakingTimerRef.current) clearTimeout(speakingTimerRef.current)
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
