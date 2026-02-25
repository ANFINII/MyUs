import { useState, useRef, useEffect, useCallback, useMemo, FormEvent } from 'react'
import { useRouter } from 'next/router'
import { ChatMessage, ChatDetailOut } from 'types/internal/media/detail'
import { LikeMediaIn, SubscribeIn } from 'types/internal/user'
import { postLikeMedia, postSubscribe } from 'api/internal/user'
import { FetchError, MediaType } from 'utils/constants/enum'
import { camelSnake } from 'utils/functions/convertCase'
import { useChatWebSocket } from 'components/hooks/useChatWebSocket'
import { useNavResize } from 'components/hooks/useNavResize'
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
  const { navRef, handleNavToggle, handleResizeStart } = useNavResize()
  const messageAreaRef = useRef<HTMLDivElement>(null)
  const [isModal, setIsModal] = useState<boolean>(false)
  const [isContent, setIsContent] = useState<boolean>(false)
  const [isContentExpanded, setIsContentExpanded] = useState<boolean>(false)
  const [formState, setFormState] = useState<ChatDetailState>(initFormState)
  useEffect(() => setFormState(initFormState), [router.query.ulid, initFormState])

  const { messages, message, reply, selectedMessage, joined, thread, likeCount, subscribeCount, isLike, isSubscribe } = formState
  const isThread = selectedMessage !== null
  const isPeriod = new Date(detail.period) < new Date()
  const isDisabled = isPeriod || !user.isActive
  const isFallowDisable = !user.isActive || user.ulid === detail.channel.ulid
  const headerDetail = { ...detail, joined, thread, like: likeCount, mediaUser: { ...detail.mediaUser, isLike, isSubscribe } }

  const scrollToBottom = useCallback(() => {
    if (messageAreaRef.current) {
      messageAreaRef.current.scrollTop = messageAreaRef.current.scrollHeight
    }
  }, [])

  useEffect(() => scrollToBottom(), [messages, scrollToBottom])

  const handleWsMessage = (newMessage: ChatMessage) => {
    setFormState((prev) => ({ ...prev, messages: [...prev.messages, newMessage], joined: prev.joined + 1, thread: prev.thread + 1 }))
  }

  const { send } = useChatWebSocket({ ulid: router.query.ulid as string | undefined, onMessage: handleWsMessage, scrollToBottom })

  const handleModal = () => setIsModal(!isModal)
  const handleContentToggle = () => setIsContent(!isContent)
  const handleContentExpand = () => setIsContentExpanded(!isContentExpanded)
  const handleThreadToggle = (message: ChatMessage | null = null) => setFormState((prev) => ({ ...prev, selectedMessage: message }))
  const handleThreadClose = () => handleThreadToggle()
  const handleMessageChange = (value: string) => setFormState((prev) => ({ ...prev, message: value }))
  const handleReplyChange = (value: string) => setFormState((prev) => ({ ...prev, reply: value }))

  const handleMessageSubmit = (e: FormEvent) => {
    e.preventDefault()
    if (message.trim().length === 0) return
    send(camelSnake({ command: 'create_message', chatId: detail.ulid, message, delta: '' }))
    setFormState((prev) => ({ ...prev, message: '' }))
  }

  const handleReplySubmit = (e: FormEvent) => {
    e.preventDefault()
    if (!selectedMessage || reply.trim().length === 0) return
    send(camelSnake({ command: 'create_reply_message', chatId: detail.ulid, message: reply, delta: '', parentId: selectedMessage.ulid }))
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
            detail={headerDetail}
            user={user}
            subscribeCount={subscribeCount}
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
