import { Search, Chat } from 'types/media'
import Layout from 'components/layout'
import ArticleChat from 'components/widgets/Article/Chat'

interface Props {
  search?: Search
  datas: Chat[]
}

export default function Chats(props: Props) {
  const { search, datas } = props

  return (
    <Layout title="Chat" search={search}>
      <article className="article_list">
        {datas.map((data) => (
          <ArticleChat data={data} key={data.id} />
        ))}
      </article>
    </Layout>
  )
}
