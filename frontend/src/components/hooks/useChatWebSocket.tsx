import { useEffect, useEffectEvent } from 'react'
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
    const ws = new WebSocket(`${wsScheme}://${apiUrl.host}/ws/chat/detail/${ulid}`)

    ws.onmessage = (event: MessageEvent<string>) => {
      handleChatEvent(snakeCamel(JSON.parse(event.data)) as ChatEvent)
    }

    return () => {
      ws.close()
    }
  }, [ulid])
}
