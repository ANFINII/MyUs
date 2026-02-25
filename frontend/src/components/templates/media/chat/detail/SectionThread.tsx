import { FormEvent } from 'react'
import clsx from 'clsx'
import { ChatMessage } from 'types/internal/media/detail'
import ChatEditor from './ChatEditor'
import MessageItem from './MessageItem'
import style from './detail.module.scss'

interface Props {
  selectedMessage: ChatMessage | null
  reply: string
  isDisabled: boolean
  handleReplyChange: (value: string) => void
  handleReplySubmit: (e: FormEvent) => void
}

export default function SectionThread(props: Props): React.JSX.Element {
  const { selectedMessage, reply, isDisabled, handleReplyChange, handleReplySubmit } = props
  const isThread = selectedMessage !== null

  return (
    <div className={clsx(style.chat_section_thread, isThread && style.active)}>
      <div className={style.thread_area}>{selectedMessage && <MessageItem message={selectedMessage} />}</div>
      <footer className={style.thread_footer}>
        <form onSubmit={handleReplySubmit}>
          <ChatEditor value={reply} onChange={handleReplyChange} disabled={isDisabled} />
        </form>
      </footer>
    </div>
  )
}
