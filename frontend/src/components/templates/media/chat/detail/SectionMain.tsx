import { FormEvent, RefObject } from 'react'
import { ChatMessage } from 'types/internal/media/detail'
import IconCaret from 'components/parts/Icon/Caret'
import MessageItem from './MessageItem'
import style from './detail.module.scss'

interface Props {
  messageAreaRef: RefObject<HTMLDivElement | null>
  messages: ChatMessage[]
  message: string
  isPeriod: boolean
  isDisabled: boolean
  isUserActive: boolean
  handleMessageChange: (value: string) => void
  handleMessageSubmit: (e: FormEvent) => void
  handleThreadToggle: (message: ChatMessage) => void
}

export default function SectionMain(props: Props): React.JSX.Element {
  const { messageAreaRef, messages, message, isPeriod, isDisabled, isUserActive, handleMessageChange, handleMessageSubmit, handleThreadToggle } = props

  return (
    <div className={style.chat_section_main}>
      <div ref={messageAreaRef} className={style.message_area}>
        {messages.map((msg) => (
          <MessageItem key={msg.ulid} message={msg} onThreadToggle={handleThreadToggle} />
        ))}
      </div>
      <footer className={style.chat_footer}>
        <form onSubmit={handleMessageSubmit}>
          <div className={style.message_input}>
            <textarea
              className={style.message_textarea}
              value={message}
              onChange={(e) => handleMessageChange(e.target.value)}
              placeholder={isPeriod ? 'チャット期間が過ぎています!' : !isUserActive ? 'チャットするにはログインが必要です!' : 'メッセージを入力...'}
              disabled={isDisabled}
              rows={1}
            />
            <button type="submit" className={style.send_button} disabled={isDisabled || message.trim().length === 0}>
              <IconCaret size="16" type="right" />
            </button>
          </div>
        </form>
      </footer>
    </div>
  )
}
