import { Search, Media } from 'types/media'
import Layout from 'components/layout'
import ArticleTodo from 'components/widgets/Article/Todo'

interface Props {
  search?: Search
  datas: Media[]
}

export default function Todos(props: Props) {
  const { search, datas } = props

  return (
    <Layout title="Todo" search={search}>
      <article className="article_list">
        {datas.map((data) => (
          <ArticleTodo data={data} key={data.id} />
        ))}
      </article>
    </Layout>
  )
}
