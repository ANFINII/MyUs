import { useRef, useEffect } from 'react'
import { API_URL } from 'lib/config'
import { ChatMessage, ChatReply } from 'types/internal/message'
import { WsCommand } from 'utils/constants/enum'
import { snakeCamel } from 'utils/functions/convertCase'

type ChatEvent =
  | { command: WsCommand.CreateMessage; message: Omit<ChatMessage, 'replyCount'> }
  | { command: WsCommand.CreateReplyMessage; message: Omit<ChatReply, 'replyCount'> }
  | { command: WsCommand.UpdateMessage; message: { ulid: string; text: string } }
  | { command: WsCommand.DeleteMessage; message: { ulid: string } }

interface Props {
  ulid: string | undefined
  onCreateMessage: (message: ChatMessage) => void
  onCreateReply: (reply: ChatReply) => void
  onUpdateMessage: (ulid: string, text: string) => void
  onDeleteMessage: (ulid: string) => void
  scrollToBottom: () => void
}

export function useChatWebSocket(props: Props): void {
  const { ulid, onCreateMessage, onCreateReply, onUpdateMessage, onDeleteMessage, scrollToBottom } = props

  const onCreateMessageRef = useRef<(message: ChatMessage) => void>(onCreateMessage)
  const onCreateReplyRef = useRef<(reply: ChatReply) => void>(onCreateReply)
  const onUpdateMessageRef = useRef<(ulid: string, text: string) => void>(onUpdateMessage)
  const onDeleteMessageRef = useRef<(ulid: string) => void>(onDeleteMessage)
  const scrollToBottomRef = useRef<() => void>(scrollToBottom)

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

    ws.onmessage = (event: MessageEvent<string>) => {
      const data = snakeCamel(JSON.parse(event.data)) as ChatEvent

      switch (data.command) {
        case WsCommand.CreateMessage: {
          onCreateMessageRef.current({ ...data.message, replyCount: 0 })
          scrollToBottomRef.current()
          break
        }
        case WsCommand.CreateReplyMessage: {
          onCreateReplyRef.current({ ...data.message, replyCount: 0 })
          break
        }
        case WsCommand.UpdateMessage: {
          onUpdateMessageRef.current(data.message.ulid, data.message.text)
          break
        }
        case WsCommand.DeleteMessage: {
          onDeleteMessageRef.current(data.message.ulid)
          break
        }
      }
    }

    return () => {
      ws.close()
    }
  }, [ulid])
}
