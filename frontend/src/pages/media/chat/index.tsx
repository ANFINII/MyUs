import { Search, Chat } from 'types/media'
import Chats from 'components/templates/media/chat/list'

const search: Search = {
  name: 'test',
  count: 0,
}
const datas: Chat[] = []

export default function ChatsPage() {
  return <Chats search={search} datas={datas} />
}
