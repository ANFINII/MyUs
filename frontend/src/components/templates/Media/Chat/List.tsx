import {Query, ChatResponse} from 'types/media'
import Main from 'components/layout/Main'
import ArticleChat from 'components/wigets/Article/Chat'

interface Props {
  query?: Query
  datas: ChatResponse[]
}

export default function ChatList(props: Props) {
  const {query, datas} = props
  return (
    <Main title="MyUsチャット" hero="Chat" query={query}>
      <article className="article_list">
        {datas.map((data) => (
          <ArticleChat data={data} key={data.id} />
        ))}
      </article>
    </Main>
  )
}
