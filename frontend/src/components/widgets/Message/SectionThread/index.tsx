import { FormEvent, MouseEvent, RefObject } from 'react'
import clsx from 'clsx'
import { ChatMessage, ChatReply } from 'types/internal/media/detail'
import { UserMe } from 'types/internal/user'
import IconCross from 'components/parts/Icon/Cross'
import ChatEditor from '../ChatEditor'
import DateDivider from '../DateDivider'
import MessageItem from '../MessageItem'
import style from './SectionThread.module.scss'

interface Props {
  user: UserMe
  selectedMessage: ChatMessage | null
  replies: ChatReply[]
  reply: string
  isDisabled: boolean
  threadRef: RefObject<HTMLDivElement | null>
  onClose: () => void
  onResize: (e: MouseEvent) => void
  onChange: (value: string) => void
  onSubmit: (e: FormEvent) => void
  onEdit: (ulid: string, text: string) => void
  onDelete: (ulid: string) => void
}

export default function SectionThread(props: Props): React.JSX.Element {
  const { user, selectedMessage, replies, reply, isDisabled, threadRef, onClose, onResize, onChange, onSubmit, onEdit, onDelete } = props
  const isThread = selectedMessage !== null

  return (
    <div ref={threadRef} className={clsx(style.chat_section_thread, isThread && style.active)}>
      <div className={style.thread_resize} onMouseDown={onResize} />
      <div className={style.thread_header}>
        <h2>スレッド</h2>
        <IconCross size="27" onClick={onClose} className={style.thread_close} />
      </div>
      <div className={style.thread_area}>
        {selectedMessage && (
          <>
            <DateDivider created={selectedMessage.created} prevCreated={null} />
            <MessageItem user={user} message={selectedMessage} isDisabled={isDisabled} onEdit={onEdit} onDelete={onDelete} />
          </>
        )}
        {replies.map((r, index) => (
          <div key={r.ulid}>
            <DateDivider created={r.created} prevCreated={index === 0 ? selectedMessage?.created ?? null : replies[index - 1].created} />
            <MessageItem user={user} message={r} isDisabled={isDisabled} onEdit={onEdit} onDelete={onDelete} />
          </div>
        ))}
        <footer className={style.thread_footer}>
          <form onSubmit={onSubmit}>
            <ChatEditor value={reply} onChange={onChange} disabled={isDisabled} />
          </form>
        </footer>
      </div>
    </div>
  )
}
