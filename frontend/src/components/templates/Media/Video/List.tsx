import { Search, Video } from 'types/internal/media'
import Layout from 'components/layout'
import ArticleVideo from 'components/widgets/Article/Video'

interface Props {
  search?: Search
  datas: Video[]
}

export default function Videos(props: Props) {
  const { search, datas } = props

  return (
    <Layout title="Video" search={search}>
      <article className="article_list">
        {datas.map((data) => (
          <ArticleVideo data={data} key={data.id} />
        ))}
      </article>
    </Layout>
  )
}
