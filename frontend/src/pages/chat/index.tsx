import {Query, ChatResponse} from 'utils/type'
import Chatist from 'components/pages/Media/Chat/List'

export default function ChatListPage() {
  const query: Query = {
    name: "test",
    count: 0,
  }
  const datas: Array<ChatResponse> = []
  return (
    <Chatist query={query} datas={datas} />
  )
}
