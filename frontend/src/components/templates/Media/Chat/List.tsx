import { getChats } from 'api/internal/media/list'
import { Chat } from 'types/internal/media'
import { useNewDatas } from 'components/hooks/useNewList'
import Main from 'components/layout/Main'
import ArticleChat from 'components/widgets/Article/Chat'

interface Props {
  datas: Chat[]
}

export default function Chats(props: Props) {
  const { datas } = props

  const { search, newDatas } = useNewDatas<Chat[]>({ datas, getDatas: (search) => getChats(search) })

  return (
    <Main title="Chat" search={{ name: search, count: newDatas.length }}>
      <article className="article_list">
        {newDatas.map((data) => (
          <ArticleChat key={data.id} data={data} />
        ))}
      </article>
    </Main>
  )
}
