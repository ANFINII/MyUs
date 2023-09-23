import { Search, Picture } from 'types/media'
import Layout from 'components/layout'
import ArticleComic from 'components/widgets/Article/Comic'

interface Props {
  search?: Search
  datas: Picture[]
}

export default function Comics(props: Props) {
  const { search, datas } = props

  return (
    <Layout title="Comic" search={search}>
      <article className="article_list">
        {datas.map((data) => (
          <ArticleComic data={data} key={data.id} />
        ))}
      </article>
    </Layout>
  )
}
