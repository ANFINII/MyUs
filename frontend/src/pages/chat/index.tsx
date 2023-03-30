import {Query, ChatResponse} from 'utils/type'
import Chatist from 'components/pages/Media/Chat/List'

const query: Query = {
  name: 'test',
  count: 0,
}
const datas: Array<ChatResponse> = []

export default function ChatListPage() {
  return <Chatist query={query} datas={datas} />
}
