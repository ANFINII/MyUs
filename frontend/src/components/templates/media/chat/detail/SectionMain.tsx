import { FormEvent, RefObject } from 'react'
import { ChatMessage } from 'types/internal/media/detail'
import ChatEditor from './ChatEditor'
import MessageItem from './MessageItem'
import style from './detail.module.scss'

interface Props {
  messageAreaRef: RefObject<HTMLDivElement | null>
  messages: ChatMessage[]
  message: string
  isDisabled: boolean
  handleMessageChange: (value: string) => void
  handleMessageSubmit: (e: FormEvent) => void
  handleThreadToggle: (message: ChatMessage) => void
}

export default function SectionMain(props: Props): React.JSX.Element {
  const { messageAreaRef, messages, message, isDisabled, handleMessageChange, handleMessageSubmit, handleThreadToggle } = props

  return (
    <div className={style.chat_section_main}>
      <div ref={messageAreaRef} className={style.message_area}>
        {messages.map((msg) => (
          <MessageItem key={msg.ulid} message={msg} onThreadToggle={handleThreadToggle} />
        ))}
      </div>
      <footer className={style.chat_footer}>
        <form onSubmit={handleMessageSubmit}>
          <ChatEditor value={message} onChange={handleMessageChange} disabled={isDisabled} />
        </form>
      </footer>
    </div>
  )
}
