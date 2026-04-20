import { MouseEvent, RefObject } from 'react'
import { ChatMessage, ChatReply } from 'types/internal/media/output'
import { UserMe } from 'types/internal/user'
import cx from 'utils/functions/cx'
import Divide from 'components/parts/Divide'
import IconCross from 'components/parts/Icon/Cross'
import style from './SectionThread.module.scss'
import ChatEditor from '../ChatEditor'
import MessageItem from '../MessageItem'

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
  onSubmit: (e: React.SubmitEvent) => void
  onEdit: (ulid: string, text: string) => void
  onDelete: (ulid: string) => void
}

export default function SectionThread(props: Props): React.JSX.Element {
  const { user, selectedMessage, replies, reply, isDisabled, threadRef, onClose, onResize, onChange, onSubmit, onEdit, onDelete } = props
  const isThread = selectedMessage !== null

  return (
    <div ref={threadRef} className={cx(style.chat_section_thread, isThread && style.active)}>
      <div className={style.thread_resize} onMouseDown={onResize} />
      <div className={style.thread_header}>
        <h2>スレッド</h2>
        <IconCross size="27" onClick={onClose} className={style.thread_close} />
      </div>
      <div className={style.thread_area}>
        {selectedMessage && (
          <>
            <MessageItem user={user} message={selectedMessage} isDisabled={isDisabled} onEdit={onEdit} onDelete={onDelete} />
            <Divide label="返信" position="left" height="thin" marginV="mv_8" marginH="mh_8" />
          </>
        )}
        {replies.map((r) => (
          <MessageItem key={r.ulid} user={user} message={r} isDisabled={isDisabled} onEdit={onEdit} onDelete={onDelete} />
        ))}
        <footer className={style.thread_footer}>
          <form onSubmit={onSubmit}>
            <ChatEditor value={reply} onChange={onChange} disabled={isDisabled} placeholder={isDisabled ? 'ログインが必要です' : ''} />
          </form>
        </footer>
      </div>
    </div>
  )
}
