import { FormEvent, RefObject } from 'react'
import { ChatMessage } from 'types/internal/media/detail'
import { UserMe } from 'types/internal/user'
import ChatEditor from './ChatEditor'
import MessageItem from './MessageItem'
import style from './detail.module.scss'

interface Props {
  user: UserMe
  messageAreaRef: RefObject<HTMLDivElement | null>
  messages: ChatMessage[]
  message: string
  isDisabled: boolean
  onThread: (message: ChatMessage) => void
  onChange: (value: string) => void
  onSubmit: (e: FormEvent) => void
  onEdit: (ulid: string, text: string) => void
  onDelete: (ulid: string) => void
}

export default function SectionMain(props: Props): React.JSX.Element {
  const { user, messageAreaRef, messages, message, isDisabled, onThread, onChange, onSubmit, onEdit, onDelete } = props

  return (
    <div className={style.chat_section_main}>
      <div ref={messageAreaRef} className={style.message_area}>
        {messages.map((msg) => (
          <MessageItem key={msg.ulid} user={user} message={msg} isDisabled={isDisabled} onThread={onThread} onEdit={onEdit} onDelete={onDelete} />
        ))}
      </div>
      <footer className={style.chat_footer}>
        <form onSubmit={onSubmit}>
          <ChatEditor value={message} onChange={onChange} disabled={isDisabled} />
        </form>
      </footer>
    </div>
  )
}
