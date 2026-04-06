import { Chat } from 'types/internal/media'
import ChatMediaContent from 'components/widgets/Media/Content/Chat'
import style from './Chat.module.scss'

interface Props {
  item: Chat
}

export default function ChatCard(props: Props): React.JSX.Element {
  const { item } = props
  const { ulid } = item

  return (
    <section className={style.card}>
      <ChatMediaContent href={`/media/chat/${ulid}`} media={item} />
    </section>
  )
}
