import { getChats } from 'api/internal/media/list'
import { Chat } from 'types/internal/media'
import { useNewDatas } from 'components/hooks/useNewList'
import Main from 'components/layout/Main'
import ArticleMedia from 'components/widgets/Media/Article/Media'
import SectionChat from 'components/widgets/Media/Section/Chat'

interface Props {
  datas: Chat[]
}

export default function Chats(props: Props) {
  const { datas } = props

  const { search, newDatas } = useNewDatas<Chat[]>({ datas, getDatas: (search) => getChats(search) })

  return (
    <Main title="Chat" search={{ name: search, count: newDatas.length }}>
      <ArticleMedia datas={newDatas} SectionMedia={SectionChat} />
    </Main>
  )
}
