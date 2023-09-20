import { Search, ChatResponse } from 'types/media'
import Main from 'components/layout/Main'
import ArticleChat from 'components/widgets/Article/Chat'

interface Props {
  search?: Search
  datas: ChatResponse[]
}

export default function Chats(props: Props) {
  const { search, datas } = props

  return (
    <Main title="Chat" search={search}>
      <article className="article_list">
        {datas.map((data) => (
          <ArticleChat data={data} key={data.id} />
        ))}
      </article>
    </Main>
  )
}
