import { Chat } from 'types/internal/media'
import ChatMediaContent from 'components/widgets/Media/Content/Chat'
import style from './Chat.module.scss'

interface Props {
  data: Chat
}

export default function ChatCard(props: Props): React.JSX.Element {
  const { data } = props
  const { ulid } = data

  return (
    <section className={style.card}>
      <ChatMediaContent href={`/media/chat/${ulid}`} media={data} />
    </section>
  )
}
