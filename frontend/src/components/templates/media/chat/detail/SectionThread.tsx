import { FormEvent } from 'react'
import clsx from 'clsx'
import { ChatMessage } from 'types/internal/media/detail'
import IconCaret from 'components/parts/Icon/Caret'
import MessageItem from './MessageItem'
import style from './detail.module.scss'

interface Props {
  selectedMessage: ChatMessage | null
  reply: string
  isPeriod: boolean
  isDisabled: boolean
  isUserActive: boolean
  handleReplyChange: (value: string) => void
  handleReplySubmit: (e: FormEvent) => void
}

export default function SectionThread(props: Props): React.JSX.Element {
  const { selectedMessage, reply, isPeriod, isDisabled, isUserActive, handleReplyChange, handleReplySubmit } = props
  const isThread = selectedMessage !== null

  return (
    <div className={clsx(style.chat_section_thread, isThread && style.active)}>
      <div className={style.thread_area}>{selectedMessage && <MessageItem message={selectedMessage} />}</div>
      <footer className={style.thread_footer}>
        <form onSubmit={handleReplySubmit}>
          <div className={style.message_input}>
            <textarea
              className={style.message_textarea}
              value={reply}
              onChange={(e) => handleReplyChange(e.target.value)}
              placeholder={isPeriod ? 'チャット期間が過ぎています!' : !isUserActive ? 'チャットするにはログインが必要です!' : '返信を入力...'}
              disabled={isDisabled}
              rows={1}
            />
            <button type="submit" className={style.send_button} disabled={isDisabled || reply.trim().length === 0}>
              <IconCaret size="16" type="right" />
            </button>
          </div>
        </form>
      </footer>
    </div>
  )
}
