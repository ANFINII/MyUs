import { useRef, useEffect } from 'react'
import { API_URL } from 'lib/config'
import { ChatMessage, ChatReply } from 'types/internal/media/detail'
import { WsCommand } from 'utils/constants/enum'

interface Props {
  ulid: string | undefined
  onCreateMessage: (message: ChatMessage) => void
  onCreateReply: (reply: ChatReply) => void
  onUpdateMessage: (ulid: string, text: string) => void
  onDeleteMessage: (ulid: string) => void
  scrollToBottom: () => void
}

export const useChatWebSocket = (props: Props): void => {
  const { ulid, onCreateMessage, onCreateReply, onUpdateMessage, onDeleteMessage, scrollToBottom } = props

  const onCreateMessageRef = useRef(onCreateMessage)
  const onCreateReplyRef = useRef(onCreateReply)
  const onUpdateMessageRef = useRef(onUpdateMessage)
  const onDeleteMessageRef = useRef(onDeleteMessage)
  const scrollToBottomRef = useRef(scrollToBottom)

  onCreateMessageRef.current = onCreateMessage
  onCreateReplyRef.current = onCreateReply
  onUpdateMessageRef.current = onUpdateMessage
  onDeleteMessageRef.current = onDeleteMessage
  scrollToBottomRef.current = scrollToBottom

  useEffect(() => {
    if (!ulid) return

    const apiUrl = new URL(API_URL)
    const wsScheme = apiUrl.protocol === 'https:' ? 'wss' : 'ws'
    const ws = new WebSocket(`${wsScheme}://${apiUrl.host}/ws/chat/detail/${ulid}`)

    ws.onmessage = (event) => {
      const eventData = JSON.parse(event.data)
      const data = eventData.message

      switch (eventData.command) {
        case WsCommand.CreateMessage: {
          const { ulid, text, created, updated, author } = data
          onCreateMessageRef.current({ ulid, text, created, updated, author })
          scrollToBottomRef.current()
          break
        }
        case WsCommand.CreateReplyMessage: {
          const { ulid, text, created, updated, author, parent_ulid: parentUlid } = data
          onCreateReplyRef.current({ ulid, text, created, updated, author, parentUlid })
          break
        }
        case WsCommand.UpdateMessage: {
          onUpdateMessageRef.current(data.ulid, data.text)
          break
        }
        case WsCommand.DeleteMessage: {
          onDeleteMessageRef.current(data.ulid)
          break
        }
      }
    }

    return () => {
      ws.close()
    }
  }, [ulid])
}
