import { useState, useRef, useEffect, useCallback, useMemo, FormEvent, MouseEvent } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/router'
import clsx from 'clsx'
import { ChatMessage, ChatDetailOut } from 'types/internal/media/detail'
import { LikeMediaIn, SubscribeIn } from 'types/internal/user'
import { postLikeMedia, postSubscribe } from 'api/internal/user'
import { FetchError, MediaType } from 'utils/constants/enum'
import { camelSnake } from 'utils/functions/convertCase'
import { formatDatetime } from 'utils/functions/datetime'
import { useToast } from 'components/hooks/useToast'
import { useUser } from 'components/hooks/useUser'
import Main from 'components/layout/Main'
import Avatar from 'components/parts/Avatar'
import AvatarLink from 'components/parts/Avatar/Link'
import Button from 'components/parts/Button'
import IconCaret from 'components/parts/Icon/Caret'
import IconChat from 'components/parts/Icon/Chat'
import IconCross from 'components/parts/Icon/Cross'
import IconHand from 'components/parts/Icon/Hand'
import IconPerson from 'components/parts/Icon/Person'
import IconResize from 'components/parts/Icon/Resize'
import SubscribeDeleteModal from 'components/widgets/Modal/SubscribeDelete'
import style from './detail.module.scss'

function len(s: string): number {
  return s.length
}

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
    if (!wsRef.current || len(message.trim()) === 0) return
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
    if (!wsRef.current || !selectedMessage || len(reply.trim()) === 0) return
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
        {/* ヘッダー行 */}
        <div className={style.header_row}>
          <div className={style.chat_section_header}>
            <div className={style.content_toggle} onClick={handleContentToggle}>
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" className={style.content_icon} fill="currentColor" viewBox="0 0 16 16">
                <path d="M5 4a.5.5 0 0 0 0 1h6a.5.5 0 0 0 0-1H5zm-.5 2.5A.5.5 0 0 1 5 6h6a.5.5 0 0 1 0 1H5a.5.5 0 0 1-.5-.5zM5 8a.5.5 0 0 0 0 1h6a.5.5 0 0 0 0-1H5zm0 2a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1H5z" />
                <path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2zm10-1H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1z" />
              </svg>
              <h1 title={detail.title}>{detail.title}</h1>
            </div>

            {/* コンテンツオーバーレイ */}
            <div className={clsx(style.content_overlay, isContent && style.active)}>
              <div className={style.content_author}>
                <AvatarLink src={detail.channel.avatar} size="m" ulid={detail.channel.ulid} nickname={detail.channel.name} />
                <div className={style.detail}>
                  <div className={style.info}>
                    <p>{detail.channel.name}</p>
                    <time>{formatDatetime(detail.created)}</time>
                  </div>
                  <div className={style.follower}>
                    登録者数 <span>{subscribeCount}</span>
                  </div>
                </div>
                <div className={style.follow}>
                  {!isSubscribe && <Button color="green" name="チャンネル登録" disabled={isFallowDisable} onClick={handleSubscribe} />}
                  {isSubscribe && <Button color="white" name="登録済み" onClick={handleModal} />}
                </div>
              </div>
              <span className={style.content_expand_toggle} onClick={handleContentExpand}>
                {isContentExpanded ? '縮小表示' : '拡大表示'}
              </span>
              <div className={clsx(style.content_body, isContentExpanded && style.expanded)}>{detail.content}</div>
            </div>

            {/* メディア情報 */}
            <div className={style.media_detail_aria}>
              <span className={style.stat_item}>
                <IconCaret size="14" />
                <span>{detail.read.toLocaleString()}</span>
              </span>
              <span className={style.stat_item}>
                <IconPerson size="14" type="base" />
                <span>{joined.toLocaleString()}</span>
              </span>
              <span className={style.stat_item}>
                <IconChat size="14" />
                <span>{thread.toLocaleString()}</span>
              </span>
              {user.isActive ? (
                <button className={style.like_button} onClick={handleLike}>
                  <IconHand size="14" type={isLike ? 'on' : 'off'} />
                  <span>{likeCount.toLocaleString()}</span>
                </button>
              ) : (
                <span className={style.stat_item}>
                  <IconHand size="14" type="off" />
                  <span>{likeCount.toLocaleString()}</span>
                </span>
              )}
              <span className={style.stat_item}>
                <time>期間 {formatDatetime(detail.period)}</time>
              </span>
            </div>
          </div>

          {/* スレッドヘッダー */}
          <div className={clsx(style.thread_header, isThread && style.active)}>
            <h2>スレッド</h2>
            <IconCross size="27" onClick={() => handleThreadToggle()} className={style.thread_close} />
          </div>
        </div>

        {/* ボディ行 */}
        <div className={style.body_row}>
          {/* サイドナビ */}
          <div ref={navRef} className={style.chat_section_nav}>
            <div className={style.nav_toggle} onClick={handleNavToggle}>
              <IconResize size="16" />
            </div>
            <div className={style.nav_area}>
              {list.map((item) => (
                <div key={item.ulid} className={style.nav_item}>
                  <Avatar src={item.channel.avatar} size="40" />
                  <Link href={`/media/chat/${item.ulid}`}>
                    <h3 className={style.nav_title} title={item.title}>
                      {item.title}
                    </h3>
                  </Link>
                </div>
              ))}
            </div>
            <div className={style.nav_resize} onMouseDown={handleResizeStart} />
          </div>

          {/* メインメッセージエリア */}
          <div className={style.chat_section_main}>
            <div ref={messageAreaRef} className={style.message_area}>
              {messages.map((message) => (
                <div key={message.ulid} className={style.message_item}>
                  <AvatarLink src={message.author.avatar} size="m" ulid={message.author.ulid} nickname={message.author.nickname} />
                  <div className={style.message_content}>
                    <div className={style.message_meta}>
                      <p>{message.author.nickname}</p>
                      <time>{formatDatetime(message.created)}</time>
                    </div>
                    <div className={style.message_text} dangerouslySetInnerHTML={{ __html: message.text }} />
                    <div className={style.message_thread_link} onClick={() => handleThreadToggle(message)}>
                      スレッド表示
                    </div>
                  </div>
                </div>
              ))}
            </div>
            <footer className={style.chat_footer}>
              <form onSubmit={handleMessageSubmit}>
                <div className={style.message_input}>
                  <textarea
                    className={style.message_textarea}
                    value={message}
                    onChange={(e) => setFormState((prev) => ({ ...prev, message: e.target.value }))}
                    placeholder={isPeriod ? 'チャット期間が過ぎています!' : !user.isActive ? 'チャットするにはログインが必要です!' : 'メッセージを入力...'}
                    disabled={isDisabled}
                    rows={1}
                  />
                  <button type="submit" className={style.send_button} disabled={isDisabled || len(message.trim()) === 0}>
                    <IconCaret size="16" type="right" />
                  </button>
                </div>
              </form>
            </footer>
          </div>

          {/* スレッドエリア */}
          <div className={clsx(style.chat_section_thread, isThread && style.active)}>
            <div className={style.thread_area}>
              {selectedMessage && (
                <div className={style.message_item}>
                  <AvatarLink src={selectedMessage.author.avatar} size="m" ulid={selectedMessage.author.ulid} nickname={selectedMessage.author.nickname} />
                  <div className={style.message_content}>
                    <div className={style.message_meta}>
                      <p>{selectedMessage.author.nickname}</p>
                      <time>{formatDatetime(selectedMessage.created)}</time>
                    </div>
                    <div className={style.message_text} dangerouslySetInnerHTML={{ __html: selectedMessage.text }} />
                  </div>
                </div>
              )}
            </div>
            <footer className={style.thread_footer}>
              <form onSubmit={handleReplySubmit}>
                <div className={style.message_input}>
                  <textarea
                    className={style.message_textarea}
                    value={reply}
                    onChange={(e) => setFormState((prev) => ({ ...prev, reply: e.target.value }))}
                    placeholder={isPeriod ? 'チャット期間が過ぎています!' : !user.isActive ? 'チャットするにはログインが必要です!' : '返信を入力...'}
                    disabled={isDisabled}
                    rows={1}
                  />
                  <button type="submit" className={style.send_button} disabled={isDisabled || len(reply.trim()) === 0}>
                    <IconCaret size="16" type="right" />
                  </button>
                </div>
              </form>
            </footer>
          </div>
        </div>
      </div>
      <SubscribeDeleteModal open={isModal} onClose={handleModal} loading={false} onAction={handleSubscribe} channel={detail.channel} followerCount={subscribeCount} />
    </Main>
  )
}
