import { useState, useRef, useEffect, useCallback, useMemo, FormEvent, MouseEvent } from 'react'
import { useRouter } from 'next/router'
import { ChatMessage, ChatDetailOut } from 'types/internal/media/detail'
import { LikeMediaIn, SubscribeIn } from 'types/internal/user'
import { postLikeMedia, postSubscribe } from 'api/internal/user'
import { FetchError, MediaType } from 'utils/constants/enum'
import { camelSnake } from 'utils/functions/convertCase'
import { useToast } from 'components/hooks/useToast'
import { useUser } from 'components/hooks/useUser'
import Main from 'components/layout/Main'
import SubscribeDeleteModal from 'components/widgets/Modal/SubscribeDelete'
import SectionHeader from './SectionHeader'
import SectionMain from './SectionMain'
import SectionNav from './SectionNav'
import SectionThread from './SectionThread'
import style from './detail.module.scss'

interface ChatDetailState {
  messages: ChatMessage[]
  message: string
  reply: string
  selectedMessage: ChatMessage | null
  joined: number
  thread: number
  likeCount: number
  subscribeCount: number
  isLike: boolean
  isSubscribe: boolean
}

interface Props {
  data: ChatDetailOut
}

export default function ChatDetail(props: Props): React.JSX.Element {
  const { data } = props
  const { detail, list } = data

  const initFormState: ChatDetailState = useMemo(
    () => ({
      messages: detail.messages,
      message: '',
      reply: '',
      selectedMessage: null,
      joined: detail.joined,
      thread: detail.thread,
      likeCount: detail.like,
      subscribeCount: 0,
      isLike: detail.mediaUser.isLike,
      isSubscribe: detail.mediaUser.isSubscribe,
    }),
    [detail],
  )

  const router = useRouter()
  const { user } = useUser()
  const { toast, handleToast } = useToast()
  const wsRef = useRef<WebSocket | null>(null)
  const navRef = useRef<HTMLDivElement>(null)
  const navWidthRef = useRef(52)
  const isDraggingRef = useRef(false)
  const messageAreaRef = useRef<HTMLDivElement>(null)
  const [isModal, setIsModal] = useState<boolean>(false)
  const [isContent, setIsContent] = useState<boolean>(false)
  const [isContentExpanded, setIsContentExpanded] = useState<boolean>(false)
  const [formState, setFormState] = useState<ChatDetailState>(initFormState)
  useEffect(() => setFormState(initFormState), [router.query.ulid, initFormState])

  const { messages, message, reply, selectedMessage, joined, thread, likeCount, subscribeCount, isLike, isSubscribe } = formState
  const NAV_MIN = 52
  const NAV_MAX_RATIO = 0.5
  const isThread = selectedMessage !== null
  const isPeriod = new Date(detail.period) < new Date()
  const isDisabled = isPeriod || !user.isActive
  const isFallowDisable = !user.isActive || user.ulid === detail.channel.ulid

  const scrollToBottom = useCallback(() => {
    if (messageAreaRef.current) {
      messageAreaRef.current.scrollTop = messageAreaRef.current.scrollHeight
    }
  }, [])

  useEffect(() => scrollToBottom(), [messages, scrollToBottom])

  // WebSocket接続
  useEffect(() => {
    const ulid = router.query.ulid
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
        setFormState((prev) => ({ ...prev, messages: [...prev.messages, newMessage], joined: prev.joined + 1, thread: prev.thread + 1 }))
        scrollToBottom()
      }
    }

    return () => {
      ws.close()
    }
  }, [router.query.ulid, scrollToBottom])

  const handleModal = () => setIsModal(!isModal)
  const handleContentToggle = () => setIsContent(!isContent)
  const handleContentExpand = () => setIsContentExpanded(!isContentExpanded)
  const handleThreadToggle = (message: ChatMessage | null = null) => setFormState((prev) => ({ ...prev, selectedMessage: message }))
  const handleThreadClose = () => handleThreadToggle()
  const handleMessageChange = (value: string) => setFormState((prev) => ({ ...prev, message: value }))
  const handleReplyChange = (value: string) => setFormState((prev) => ({ ...prev, reply: value }))

  const setNavWidth = useCallback((width: number) => {
    navWidthRef.current = width
    if (navRef.current) {
      navRef.current.style.width = `${width}px`
    }
  }, [])

  const handleNavToggle = () => {
    const half = (window.innerWidth - 72) / 2
    setNavWidth(navWidthRef.current > NAV_MIN ? NAV_MIN : half)
  }

  const handleResizeStart = useCallback(
    (e: MouseEvent) => {
      e.preventDefault()
      isDraggingRef.current = true
      document.body.style.cursor = 'col-resize'
      document.body.style.userSelect = 'none'

      const handleMouseMove = (moveEvent: globalThis.MouseEvent) => {
        if (!isDraggingRef.current) return
        const sidebarLeft = 72
        const newWidth = moveEvent.clientX - sidebarLeft
        const maxWidth = window.innerWidth * NAV_MAX_RATIO
        setNavWidth(Math.max(NAV_MIN, Math.min(newWidth, maxWidth)))
      }

      const handleMouseUp = () => {
        isDraggingRef.current = false
        document.body.style.cursor = ''
        document.body.style.userSelect = ''
        document.removeEventListener('mousemove', handleMouseMove)
        document.removeEventListener('mouseup', handleMouseUp)
      }

      document.addEventListener('mousemove', handleMouseMove)
      document.addEventListener('mouseup', handleMouseUp)
    },
    [setNavWidth],
  )

  const handleMessageSubmit = (e: FormEvent) => {
    e.preventDefault()
    if (!wsRef.current || message.trim().length === 0) return
    wsRef.current.send(
      JSON.stringify(
        camelSnake({
          command: 'create_message',
          chatId: detail.ulid,
          message: message,
          delta: '',
        }),
      ),
    )
    setFormState((prev) => ({ ...prev, message: '' }))
  }

  const handleReplySubmit = (e: FormEvent) => {
    e.preventDefault()
    if (!wsRef.current || !selectedMessage || reply.trim().length === 0) return
    wsRef.current.send(
      JSON.stringify(
        camelSnake({
          command: 'create_reply_message',
          chatId: detail.ulid,
          message: reply,
          delta: '',
          parentId: selectedMessage.ulid,
        }),
      ),
    )
    setFormState((prev) => ({ ...prev, reply: '' }))
  }

  const handleLike = async () => {
    const ulid = String(router.query.ulid)
    const request: LikeMediaIn = { ulid, mediaType: MediaType.Chat }
    const ret = await postLikeMedia(request)
    if (ret.isErr()) return handleToast(FetchError.Post, true)
    const data = ret.value
    setFormState((prev) => ({ ...prev, ...data }))
  }

  const fetchSubscribe = async (isSubscribe: boolean) => {
    const request: SubscribeIn = { channelUlid: detail.channel.ulid, isSubscribe }
    const ret = await postSubscribe(request)
    if (ret.isErr()) return handleToast(FetchError.Post, true)
    const data = ret.value
    setFormState((prev) => ({ ...prev, isSubscribe: data.isSubscribe, subscribeCount: data.count }))
  }

  const handleSubscribe = async () => {
    await fetchSubscribe(!isSubscribe)
    if (isSubscribe) handleModal()
    handleToast(isSubscribe ? 'チャンネル登録を解除しました' : 'チャンネルを登録しました', false)
  }

  if (!detail.publish) {
    return (
      <Main metaTitle="Chat" toast={toast}>
        <article>
          <h2 className={style.unpublished}>非公開に設定されてます!</h2>
        </article>
      </Main>
    )
  }

  return (
    <Main metaTitle="Chat" toast={toast}>
      <div className={style.chat_section}>
        <div className={style.header_row}>
          <SectionHeader
            detail={detail}
            user={user}
            joined={joined}
            thread={thread}
            likeCount={likeCount}
            subscribeCount={subscribeCount}
            isLike={isLike}
            isSubscribe={isSubscribe}
            isThread={isThread}
            isContent={isContent}
            isContentExpanded={isContentExpanded}
            isFallowDisable={isFallowDisable}
            handleContentToggle={handleContentToggle}
            handleContentExpand={handleContentExpand}
            handleLike={handleLike}
            handleSubscribe={handleSubscribe}
            handleModal={handleModal}
            handleThreadClose={handleThreadClose}
          />
        </div>
        <div className={style.body_row}>
          <SectionNav navRef={navRef} list={list} handleNavToggle={handleNavToggle} handleResizeStart={handleResizeStart} />
          <SectionMain
            messageAreaRef={messageAreaRef}
            messages={messages}
            message={message}
            isPeriod={isPeriod}
            isDisabled={isDisabled}
            isUserActive={user.isActive}
            handleMessageChange={handleMessageChange}
            handleMessageSubmit={handleMessageSubmit}
            handleThreadToggle={handleThreadToggle}
          />
          <SectionThread
            selectedMessage={selectedMessage}
            reply={reply}
            isPeriod={isPeriod}
            isDisabled={isDisabled}
            isUserActive={user.isActive}
            handleReplyChange={handleReplyChange}
            handleReplySubmit={handleReplySubmit}
          />
        </div>
      </div>
      <SubscribeDeleteModal open={isModal} onClose={handleModal} loading={false} onAction={handleSubscribe} channel={detail.channel} followerCount={subscribeCount} />
    </Main>
  )
}
