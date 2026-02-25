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
  onChange: (value: string) => void
  onSubmit: (e: FormEvent) => void
}

export default function SectionThread(props: Props): React.JSX.Element {
  const { selectedMessage, reply, isDisabled, onChange, onSubmit } = props
  const isThread = selectedMessage !== null

  return (
    <div className={clsx(style.chat_section_thread, isThread && style.active)}>
      <div className={style.thread_area}>{selectedMessage && <MessageItem message={selectedMessage} />}</div>
      <footer className={style.thread_footer}>
        <form onSubmit={onSubmit}>
          <ChatEditor value={reply} onChange={onChange} disabled={isDisabled} />
        </form>
      </footer>
    </div>
  )
}
