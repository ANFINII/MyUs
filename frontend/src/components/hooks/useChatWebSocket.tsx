import { useRef, useEffect } from 'react'
import { API_URL } from 'lib/config'
import { ChatMessage, ChatReply } from 'types/internal/message'
import { WsCommand } from 'utils/constants/enum'

// サーバー（usecase/broadcast.py）から届くデータ。キーは snake_case のまま届く
interface AuthorPayload {
  avatar: string
  ulid: string
  nickname: string
  follower_count: number
}

interface MessagePayload {
  ulid: string
  text: string
  created: Date
  updated: Date
  author: AuthorPayload
}

interface ReplyPayload extends MessagePayload {
  parent_ulid: string
}

type ChatEvent =
  | { command: WsCommand.CreateMessage; message: MessagePayload }
  | { command: WsCommand.CreateReplyMessage; message: ReplyPayload }
  | { command: WsCommand.UpdateMessage; message: { ulid: string; text: string } }
  | { command: WsCommand.DeleteMessage; message: { ulid: string } }

const toChatMessage = (payload: MessagePayload): ChatMessage => {
  const { ulid, text, created, updated, author } = payload
  const { avatar, nickname, follower_count: followerCount } = author
  return { ulid, text, replyCount: 0, created, updated, author: { avatar, ulid: author.ulid, nickname, followerCount } }
}

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
      const data: ChatEvent = JSON.parse(event.data)

      switch (data.command) {
        case WsCommand.CreateMessage: {
          onCreateMessageRef.current(toChatMessage(data.message))
          scrollToBottomRef.current()
          break
        }
        case WsCommand.CreateReplyMessage: {
          onCreateReplyRef.current({ ...toChatMessage(data.message), parentUlid: data.message.parent_ulid })
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
