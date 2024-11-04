import { Chat } from 'types/internal/media'
import { getChats } from 'api/internal/media/list'
import { useNewDatas } from 'components/hooks/useNewList'
import Main from 'components/layout/Main'
import MediaList from 'components/widgets/Media/List/Media'
import MediaChat from 'components/widgets/Media/Index/Chat'

interface Props {
  datas: Chat[]
}

export default function Chats(props: Props) {
  const { datas } = props

  const { search, newDatas } = useNewDatas<Chat[]>({ datas, getDatas: (search) => getChats(search) })

  return (
    <Main title="Chat" search={{ name: search, count: newDatas.length }}>
      <MediaList datas={newDatas} MediaMedia={MediaChat} />
    </Main>
  )
}
