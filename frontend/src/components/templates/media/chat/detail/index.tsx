import { useState, useRef, useEffect, useCallback, useMemo, FormEvent } from 'react'
import { useRouter } from 'next/router'
import { ChatMessage, ChatReply, ChatDetailOut, MessageCreateIn, MessageUpdateIn } from 'types/internal/media/detail'
import { LikeMediaIn, SubscribeIn } from 'types/internal/user'
import { postMessage, getReplies, putMessage, deleteMessage } from 'api/internal/media/message'
import { postLikeMedia, postSubscribe } from 'api/internal/user'
import { FetchError, MediaType } from 'utils/constants/enum'
import { useChatWebSocket } from 'components/hooks/useChatWebSocket'
import { useNavResize } from 'components/hooks/useNavResize'
import { useToast } from 'components/hooks/useToast'
import { useUser } from 'components/hooks/useUser'
import Main from 'components/layout/Main'
import SubscribeDeleteModal from 'components/widgets/Modal/SubscribeDelete'
import SectionContent from './SectionContent'
import SectionHeader from './SectionHeader'
import SectionMain from './SectionMain'
import SectionNav from './SectionNav'
import SectionThread from './SectionThread'
import style from './detail.module.scss'

interface ChatDetailState {
  messages: ChatMessage[]
  replies: Record<string, ChatReply[]>
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
      replies: {},
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
  const { navRef, handleNav, handleResize } = useNavResize()
  const messageAreaRef = useRef<HTMLDivElement>(null)
  const [isModal, setIsModal] = useState<boolean>(false)
  const [isContent, setIsContent] = useState<boolean>(false)
  const [isContentExpand, setIsContentExpand] = useState<boolean>(false)
  const [formState, setFormState] = useState<ChatDetailState>(initFormState)
  useEffect(() => setFormState(initFormState), [router.query.ulid, initFormState])

  const { messages, replies, message, reply, selectedMessage, joined, thread, likeCount, subscribeCount, isLike, isSubscribe } = formState
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

  const handleWsCreateMessage = (newMessage: ChatMessage) => {
    setFormState((prev) => {
      if (prev.messages.some((m) => m.ulid === newMessage.ulid)) return prev
      return { ...prev, messages: [...prev.messages, newMessage], joined: prev.joined + 1, thread: prev.thread + 1 }
    })
  }

  const handleWsCreateReply = (newReply: ChatReply) => {
    setFormState((prev) => {
      const existing = prev.replies[newReply.parentUlid] ?? []
      if (existing.some((r) => r.ulid === newReply.ulid)) return prev
      return {
        ...prev,
        replies: {
          ...prev.replies,
          [newReply.parentUlid]: [...existing, newReply],
        },
      }
    })
  }

  const handleWsUpdateMessage = (ulid: string, text: string) => {
    setFormState((prev) => ({
      ...prev,
      messages: prev.messages.map((m) => (m.ulid === ulid ? { ...m, text } : m)),
      replies: Object.fromEntries(
        Object.entries(prev.replies).map(([key, list]) => [key, list.map((r) => (r.ulid === ulid ? { ...r, text } : r))]),
      ),
    }))
  }

  const handleWsDeleteMessage = (ulid: string) => {
    setFormState((prev) => ({
      ...prev,
      messages: prev.messages.filter((m) => m.ulid !== ulid),
      replies: Object.fromEntries(Object.entries(prev.replies).map(([key, list]) => [key, list.filter((r) => r.ulid !== ulid)])),
    }))
  }

  useChatWebSocket({
    ulid: router.query.ulid as string | undefined,
    onCreateMessage: handleWsCreateMessage,
    onCreateReply: handleWsCreateReply,
    onUpdateMessage: handleWsUpdateMessage,
    onDeleteMessage: handleWsDeleteMessage,
    scrollToBottom,
  })

  const handleModal = () => setIsModal(!isModal)
  const handleContent = () => setIsContent(!isContent)
  const handleContentExpand = () => setIsContentExpand(!isContentExpand)
  const handleMessage = (value: string) => setFormState((prev) => ({ ...prev, message: value }))
  const handleReply = (value: string) => setFormState((prev) => ({ ...prev, reply: value }))

  const handleThread = async (message: ChatMessage | null = null) => {
    if (message !== null) {
      const ret = await getReplies(message.ulid)
      if (ret.isOk()) {
        const replyData: ChatReply[] = ret.value.map((r) => ({ ...r, parentUlid: message.ulid }))
        setFormState((prev) => ({
          ...prev,
          selectedMessage: message,
          replies: { ...prev.replies, [message.ulid]: replyData },
        }))
        return
      }
    }
    setFormState((prev) => ({ ...prev, selectedMessage: message }))
  }

  const handleEditMessage = async (ulid: string, text: string) => {
    const request: MessageUpdateIn = { chatUlid: detail.ulid, text }
    const ret = await putMessage(ulid, request)
    if (ret.isErr()) return handleToast(FetchError.Put, true)
  }

  const handleDeleteMessage = async (ulid: string) => {
    const ret = await deleteMessage(ulid)
    if (ret.isErr()) return handleToast(FetchError.Delete, true)
  }

  const handleMessageSubmit = async (e: FormEvent) => {
    e.preventDefault()
    if (message.replace(/<[^>]*>/g, '').trim().length === 0) return
    const request: MessageCreateIn = { chatUlid: detail.ulid, text: message }
    const ret = await postMessage(request)
    if (ret.isErr()) return handleToast(FetchError.Post, true)
    setFormState((prev) => ({ ...prev, message: '' }))
  }

  const handleReplySubmit = async (e: FormEvent) => {
    e.preventDefault()
    if (!selectedMessage || reply.replace(/<[^>]*>/g, '').trim().length === 0) return
    const request: MessageCreateIn = { chatUlid: detail.ulid, text: reply, parentUlid: selectedMessage.ulid }
    const ret = await postMessage(request)
    if (ret.isErr()) return handleToast(FetchError.Post, true)
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

  const handleSubscribe = async () => {
    const request: SubscribeIn = { channelUlid: detail.channel.ulid, isSubscribe: !isSubscribe }
    const ret = await postSubscribe(request)
    if (ret.isErr()) return handleToast(FetchError.Post, true)
    const data = ret.value
    setFormState((prev) => ({ ...prev, isSubscribe: data.isSubscribe, subscribeCount: data.count }))
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
        <div className={style.body_row}>
          <SectionNav navRef={navRef} list={list} onNav={handleNav} onResize={handleResize} />
          <div className={style.main_column}>
            <SectionHeader detail={headerDetail} user={user} onContent={handleContent} onLike={handleLike} />
            <div className={style.main_body}>
              <SectionContent
                detail={headerDetail}
                subscribeCount={subscribeCount}
                isContent={isContent}
                isContentExpand={isContentExpand}
                isFallowDisable={isFallowDisable}
                onModal={handleModal}
                onSubscribe={handleSubscribe}
                onContentExpand={handleContentExpand}
              />
              <SectionMain
                messageAreaRef={messageAreaRef}
                messages={messages}
                message={message}
                user={user}
                isDisabled={isDisabled}
                onThread={handleThread}
                onChange={handleMessage}
                onSubmit={handleMessageSubmit}
                onEdit={handleEditMessage}
                onDelete={handleDeleteMessage}
              />
            </div>
          </div>
          <SectionThread
            selectedMessage={selectedMessage}
            replies={selectedMessage ? replies[selectedMessage.ulid] ?? [] : []}
            reply={reply}
            user={user}
            isDisabled={isDisabled}
            onClose={() => handleThread()}
            onChange={handleReply}
            onSubmit={handleReplySubmit}
            onEdit={handleEditMessage}
            onDelete={handleDeleteMessage}
          />
        </div>
      </div>
      <SubscribeDeleteModal open={isModal} onClose={handleModal} loading={false} onAction={handleSubscribe} channel={detail.channel} followerCount={subscribeCount} />
    </Main>
  )
}
