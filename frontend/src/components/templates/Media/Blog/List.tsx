import {Query, ImageResponse} from 'types/media'
import Main from 'components/layout/Main'
import ArticleBlog from 'components/widgets/Article/Blog'

interface Props {
  query?: Query
  datas: ImageResponse[]
}

export default function BlogList(props: Props) {
  const {query, datas} = props
  return (
    <Main title="MyUsブログ" hero="Blog" query={query}>
      <article className="article_list">
        {datas.map((data) => (
          <ArticleBlog data={data} key={data.id} />
        ))}
      </article>
    </Main>
  )
}
