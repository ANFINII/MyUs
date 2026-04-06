import { Chat } from 'types/internal/media'
import Card from 'components/parts/Card'
import style from './Chat.module.scss'
import CardChatMediaContent from '../Content/Chat'

interface Props {
  item: Chat
}

export default function ChatCard(props: Props): React.JSX.Element {
  const { item } = props
  const { ulid } = item

  return (
    <Card className={style.card}>
      <CardChatMediaContent href={`/media/chat/${ulid}`} media={item} />
    </Card>
  )
}
