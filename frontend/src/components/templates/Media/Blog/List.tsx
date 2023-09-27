import { Search, Picture } from 'types/internal/media'
import Layout from 'components/layout'
import ArticleBlog from 'components/widgets/Article/Blog'

interface Props {
  search?: Search
  datas: Picture[]
}

export default function Blogs(props: Props) {
  const { search, datas } = props

  return (
    <Layout title="Blog" search={search}>
      <article className="article_list">
        {datas.map((data) => (
          <ArticleBlog data={data} key={data.id} />
        ))}
      </article>
    </Layout>
  )
}
