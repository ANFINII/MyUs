import { useEffect, useEffectEvent } from 'react'
import { API_URL } from 'lib/config'
import { ChatMessage, ChatReply } from 'types/internal/message'
import { WsCommand } from 'utils/constants/enum'
import { snakeCamel } from 'utils/functions/convertCase'

const RECONNECT_BASE_MS = 1000
const RECONNECT_MAX_MS = 30000

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

  const handleChatEvent = useEffectEvent((data: ChatEvent) => {
    switch (data.command) {
      case WsCommand.CreateMessage: {
        onCreateMessage({ ...data.message, replyCount: 0 })
        scrollToBottom()
        break
      }
      case WsCommand.CreateReplyMessage: {
        onCreateReply({ ...data.message, replyCount: 0 })
        break
      }
      case WsCommand.UpdateMessage: {
        onUpdateMessage(data.message.ulid, data.message.text)
        break
      }
      case WsCommand.DeleteMessage: {
        onDeleteMessage(data.message.ulid)
        break
      }
    }
  })

  useEffect(() => {
    if (!ulid) return

    const apiUrl = new URL(API_URL)
    const wsScheme = apiUrl.protocol === 'https:' ? 'wss' : 'ws'
    const url = `${wsScheme}://${apiUrl.host}/ws/chat/detail/${ulid}`
    let ws: WebSocket | null = null
    let timer: ReturnType<typeof setTimeout> | null = null
    let retry = 0
    let isClosed = false

    const connect = () => {
      ws = new WebSocket(url)
      ws.onopen = () => {
        retry = 0
      }
      ws.onmessage = (event: MessageEvent<string>) => {
        handleChatEvent(snakeCamel(JSON.parse(event.data)) as ChatEvent)
      }
      ws.onclose = () => {
        if (isClosed) return
        timer = setTimeout(connect, Math.min(RECONNECT_BASE_MS * 2 ** retry, RECONNECT_MAX_MS))
        retry += 1
      }
    }

    connect()

    return () => {
      isClosed = true
      if (timer) clearTimeout(timer)
      ws?.close()
    }
  }, [ulid])
}
