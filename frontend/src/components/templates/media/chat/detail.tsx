import { useState, useRef, useEffect, useCallback, ChangeEvent, FormEvent, MouseEvent } from 'react'
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
import SubscribeDeleteModal from 'components/widgets/Modal/SubscribeDelete'
import style from './detail.module.scss'

interface Props {
  data: ChatDetailOut
}

export default function ChatDetail(props: Props): React.JSX.Element {
  const { data } = props
  const { detail, list } = data

  const router = useRouter()
  const { user } = useUser()
  const { toast, handleToast } = useToast()

  const [isContentOpen, setIsContentOpen] = useState(false)
  const [isContentExpanded, setIsContentExpanded] = useState(false)
  const [isThreadOpen, setIsThreadOpen] = useState(false)
  const [selectedMessage, setSelectedMessage] = useState<ChatMessage | null>(null)
  const [messageText, setMessageText] = useState('')
  const [replyText, setReplyText] = useState('')
  const [messages, setMessages] = useState<ChatMessage[]>(detail.messages)
  const [joined, setJoined] = useState(detail.joined)
  const [thread, setThread] = useState(detail.thread)
  const [isLike, setIsLike] = useState(detail.mediaUser.isLike)
  const [isSubscribe, setIsSubscribe] = useState(detail.mediaUser.isSubscribe)
  const [likeCount, setLikeCount] = useState(detail.likeCount)
  const [subscribeCount, setSubscribeCount] = useState(0)
  const [isModal, setIsModal] = useState(false)

  const messageAreaRef = useRef<HTMLDivElement>(null)
  const navRef = useRef<HTMLDivElement>(null)
  const navWidthRef = useRef(52)
  const wsRef = useRef<WebSocket | null>(null)
  const isDraggingRef = useRef(false)
  const NAV_MIN = 52
  const NAV_MAX_RATIO = 0.5

  const isFallowDisable = !user.isActive || user.ulid === detail.channel.ulid
  const isPeriod = new Date(detail.period) < new Date()
  const isDisabled = isPeriod || !user.isActive

  const scrollToBottom = useCallback(() => {
    if (messageAreaRef.current) {
      messageAreaRef.current.scrollTop = messageAreaRef.current.scrollHeight
    }
  }, [])

  // WebSocket接続
  useEffect(() => {
    const ulid = router.query.ulid
    if (!ulid) return

    const wsScheme = window.location.protocol === 'https:' ? 'wss' : 'ws'
    const ws = new WebSocket(`${wsScheme}://${window.location.host}/ws/chat/detail/${ulid}`)
    wsRef.current = ws

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.command === 'create_message') {
        const response = data.message
        const newMessage: ChatMessage = {
          ulid: response.ulid,
          text: response.text,
          created: response.created,
          updated: response.updated,
          author: response.author,
        }
        setMessages((prev) => [...prev, newMessage])
        setJoined(response.joined)
        setThread(response.thread)
        scrollToBottom()
      }
    }

    return () => {
      ws.close()
    }
  }, [router.query.ulid, scrollToBottom])

  useEffect(() => {
    scrollToBottom()
  }, [messages, scrollToBottom])

  const handleContentToggle = () => setIsContentOpen(!isContentOpen)
  const handleContentExpand = () => setIsContentExpanded(!isContentExpanded)
  const handleModal = () => setIsModal(!isModal)

  const setNavWidth = useCallback((width: number) => {
    navWidthRef.current = width
    if (navRef.current) {
      navRef.current.style.width = `${width}px`
    }
  }, [])

  const handleNavToggle = () => {
    setNavWidth(navWidthRef.current > NAV_MIN ? NAV_MIN : 240)
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

  const handleThreadOpen = (message: ChatMessage) => {
    setSelectedMessage(message)
    setIsThreadOpen(true)
  }

  const handleThreadClose = () => {
    setIsThreadOpen(false)
    setSelectedMessage(null)
  }

  const handleMessageSubmit = (e: FormEvent) => {
    e.preventDefault()
    if (!wsRef.current || len(messageText.trim()) === 0) return
    wsRef.current.send(
      JSON.stringify(
        camelSnake({
          command: 'create_message',
          chatId: detail.ulid,
          message: messageText,
          delta: '',
        }),
      ),
    )
    setMessageText('')
  }

  const handleReplySubmit = (e: FormEvent) => {
    e.preventDefault()
    if (!wsRef.current || !selectedMessage || len(replyText.trim()) === 0) return
    wsRef.current.send(
      JSON.stringify(
        camelSnake({
          command: 'create_reply_message',
          chatId: detail.ulid,
          message: replyText,
          delta: '',
          parentId: selectedMessage.ulid,
        }),
      ),
    )
    setReplyText('')
  }

  const handleLike = async () => {
    const ulid = String(router.query.ulid)
    const request: LikeMediaIn = { ulid, mediaType: MediaType.Chat }
    const ret = await postLikeMedia(request)
    if (ret.isErr()) return handleToast(FetchError.Post, true)
    const data = ret.value
    setIsLike(data.isLike)
    setLikeCount(data.likeCount)
  }

  const fetchSubscribe = async (isSubscribe: boolean) => {
    const request: SubscribeIn = { channelUlid: detail.channel.ulid, isSubscribe }
    const ret = await postSubscribe(request)
    if (ret.isErr()) return handleToast(FetchError.Post, true)
    const data = ret.value
    setIsSubscribe(data.isSubscribe)
    setSubscribeCount(data.count)
  }

  const handleSubscribe = async () => {
    await fetchSubscribe(true)
    handleToast('チャンネルを登録しました', false)
  }

  const handleDeleteSubscribe = async () => {
    await fetchSubscribe(false)
    handleModal()
    handleToast('チャンネル登録を解除しました', false)
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
        {/* ヘッダー */}
        <div className={clsx(style.chat_section_header, isThreadOpen && style.thread_open)}>
          <div className={style.content_toggle} onClick={handleContentToggle}>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" className={style.content_icon} fill="currentColor" viewBox="0 0 16 16">
              <path d="M5 4a.5.5 0 0 0 0 1h6a.5.5 0 0 0 0-1H5zm-.5 2.5A.5.5 0 0 1 5 6h6a.5.5 0 0 1 0 1H5a.5.5 0 0 1-.5-.5zM5 8a.5.5 0 0 0 0 1h6a.5.5 0 0 0 0-1H5zm0 2a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1H5z" />
              <path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2zm10-1H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1z" />
            </svg>
            <h1 title={detail.title}>{detail.title}</h1>
          </div>

          {/* コンテンツオーバーレイ */}
          <div className={clsx(style.content_overlay, isContentOpen && style.active)}>
            <div className={style.content_author}>
              <AvatarLink src={detail.channel.avatar} size="m" ulid={detail.channel.ulid} nickname={detail.channel.name} />
              <div className={style.content_author_info}>
                <p>{detail.channel.name}</p>
                <time>{formatDatetime(detail.created)}</time>
              </div>
              <div className={style.content_author_follower}>
                登録者数 <span>{subscribeCount}</span>
              </div>
              <div className={style.content_author_follow}>
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
        <div className={clsx(style.thread_header, isThreadOpen && style.active)}>
          <h2>スレッド</h2>
          <IconCross size="27" onClick={handleThreadClose} className={style.thread_close} />
        </div>

        {/* サイドナビ */}
        <div ref={navRef} className={style.chat_section_nav}>
          <div className={style.nav_toggle} onClick={handleNavToggle}>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
              <path
                fillRule="evenodd"
                d="M1 11.5a.5.5 0 0 0 .5.5h11.793l-3.147 3.146a.5.5 0 0 0 .708.708l4-4a.5.5 0 0 0 0-.708l-4-4a.5.5 0 0 0-.708.708L13.293 11H1.5a.5.5 0 0 0-.5.5zm14-7a.5.5 0 0 1-.5.5H2.707l3.147 3.146a.5.5 0 1 1-.708.708l-4-4a.5.5 0 0 1 0-.708l4-4a.5.5 0 1 1 .708.708L2.707 4H14.5a.5.5 0 0 1 .5.5z"
              />
            </svg>
          </div>
          <div className={style.nav_area}>
            {list.map((item) => (
              <div key={item.ulid} className={style.nav_item}>
                <Avatar src={item.channel.avatar} size="m" />
                <Link href={`/media/chat/${item.ulid}`}>
                  <h3 className={style.nav_item_title} title={item.title}>
                    {item.title}
                  </h3>
                </Link>
              </div>
            ))}
          </div>
          <div className={style.nav_resize_handle} onMouseDown={handleResizeStart} />
        </div>

        {/* メインメッセージエリア */}
        <div className={clsx(style.chat_section_main, isThreadOpen && style.thread_open)}>
          <div ref={messageAreaRef} className={style.message_area}>
            {messages.map((message) => (
              <div key={message.ulid} className={style.message_item}>
                <AvatarLink src={message.author.avatar} size="m" ulid={message.author.ulid} nickname={message.author.nickname} />
                <div className={style.message_meta}>
                  <p>{message.author.nickname}</p>
                  <time>{formatDatetime(message.created)}</time>
                </div>
                <div className={style.message_text} dangerouslySetInnerHTML={{ __html: message.text }} />
                <div className={style.message_thread_link} onClick={() => handleThreadOpen(message)}>
                  スレッド表示
                </div>
              </div>
            ))}
          </div>
          <footer className={style.chat_footer}>
            <form onSubmit={handleMessageSubmit}>
              <div className={style.message_input}>
                <textarea
                  className={style.message_textarea}
                  value={messageText}
                  onChange={(e: ChangeEvent<HTMLTextAreaElement>) => setMessageText(e.target.value)}
                  placeholder={isPeriod ? 'チャット期間が過ぎています!' : !user.isActive ? 'チャットするにはログインが必要です!' : 'メッセージを入力...'}
                  disabled={isDisabled}
                  rows={1}
                />
                <button type="submit" className={style.send_button} disabled={isDisabled || len(messageText.trim()) === 0}>
                  <IconCaret size="16" type="right" />
                </button>
              </div>
            </form>
          </footer>
        </div>

        {/* スレッドエリア */}
        <div className={clsx(style.chat_section_thread, isThreadOpen && style.active)}>
          <div className={style.thread_area}>
            {selectedMessage && (
              <div className={style.message_item}>
                <AvatarLink src={selectedMessage.author.avatar} size="m" ulid={selectedMessage.author.ulid} nickname={selectedMessage.author.nickname} />
                <div className={style.message_meta}>
                  <p>{selectedMessage.author.nickname}</p>
                  <time>{formatDatetime(selectedMessage.created)}</time>
                </div>
                <div className={style.message_text} dangerouslySetInnerHTML={{ __html: selectedMessage.text }} />
              </div>
            )}
          </div>
          <footer className={style.thread_footer}>
            <form onSubmit={handleReplySubmit}>
              <div className={style.message_input}>
                <textarea
                  className={style.message_textarea}
                  value={replyText}
                  onChange={(e: ChangeEvent<HTMLTextAreaElement>) => setReplyText(e.target.value)}
                  placeholder={isPeriod ? 'チャット期間が過ぎています!' : !user.isActive ? 'チャットするにはログインが必要です!' : '返信を入力...'}
                  disabled={isDisabled}
                  rows={1}
                />
                <button type="submit" className={style.send_button} disabled={isDisabled || len(replyText.trim()) === 0}>
                  <IconCaret size="16" type="right" />
                </button>
              </div>
            </form>
          </footer>
        </div>
      </div>

      <SubscribeDeleteModal open={isModal} onClose={handleModal} loading={false} onAction={handleDeleteSubscribe} channel={detail.channel} followerCount={subscribeCount} />
    </Main>
  )
}

function len(s: string): number {
  return s.length
}
