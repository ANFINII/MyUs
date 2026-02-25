import { useRef, useEffect, useCallback } from 'react'
import { ChatMessage } from 'types/internal/media/detail'

interface OutProps {
  send: (data: object) => void
}

interface Props {
  ulid: string | undefined
  onMessage: (message: ChatMessage) => void
  scrollToBottom: () => void
}

export const useChatWebSocket = (props: Props): OutProps => {
  const { ulid, onMessage, scrollToBottom } = props

  const wsRef = useRef<WebSocket | null>(null)
  const onMessageRef = useRef(onMessage)
  const scrollToBottomRef = useRef(scrollToBottom)

  onMessageRef.current = onMessage
  scrollToBottomRef.current = scrollToBottom

  useEffect(() => {
    if (!ulid) return

    const wsScheme = window.location.protocol === 'https:' ? 'wss' : 'ws'
    const ws = new WebSocket(`${wsScheme}://${window.location.host}/ws/chat/detail/${ulid}`)
    wsRef.current = ws

    ws.onmessage = (event) => {
      const eventData = JSON.parse(event.data)
      if (eventData.command === 'create_message') {
        const data = eventData.message
        const { ulid, text, created, updated, author } = data
        const newMessage: ChatMessage = { ulid, text, created, updated, author }
        onMessageRef.current(newMessage)
        scrollToBottomRef.current()
      }
    }

    return () => {
      ws.close()
    }
  }, [ulid])

  const send = useCallback((data: object) => {
    if (!wsRef.current) return
    wsRef.current.send(JSON.stringify(data))
  }, [])

  return { send }
}
