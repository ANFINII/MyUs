import {Query, ChatResponse} from 'utils/type'
import Main from 'components/layouts/Main'
import ArticleChat from 'components/elements/Article/Chat'

interface Props {
  query?: Query
  datas: Array<ChatResponse>
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
