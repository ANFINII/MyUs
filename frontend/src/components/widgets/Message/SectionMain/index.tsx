import { RefObject } from 'react'
import { ChatMessage } from 'types/internal/media/detail'
import { UserMe } from 'types/internal/user'
import ChatEditor from '../ChatEditor'
import DateDivider from '../DateDivider'
import MessageItem from '../MessageItem'
import style from './SectionMain.module.scss'

interface Props {
  user: UserMe
  messageAreaRef: RefObject<HTMLDivElement | null>
  messages: ChatMessage[]
  message: string
  isDisabled: boolean
  onThread: (message: ChatMessage) => void
  onChange: (value: string) => void
  onSubmit: (e: React.SubmitEvent) => void
  onEdit: (ulid: string, text: string) => void
  onDelete: (ulid: string) => void
}

export default function SectionMain(props: Props): React.JSX.Element {
  const { user, messageAreaRef, messages, message, isDisabled, onThread, onChange, onSubmit, onEdit, onDelete } = props

  return (
    <div ref={messageAreaRef} className={style.chat_section_main}>
      {messages.map((msg, index) => (
        <div key={msg.ulid}>
          <DateDivider created={msg.created} prevCreated={index > 0 ? messages[index - 1]?.created : undefined} />
          <MessageItem user={user} message={msg} isDisabled={isDisabled} onThread={onThread} onEdit={onEdit} onDelete={onDelete} />
        </div>
      ))}
      <footer className={style.chat_footer}>
        <form onSubmit={onSubmit}>
          <ChatEditor value={message} onChange={onChange} disabled={isDisabled} />
        </form>
      </footer>
    </div>
  )
}
