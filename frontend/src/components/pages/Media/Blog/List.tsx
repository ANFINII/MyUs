import {Query, ImageResponse} from 'utils/type'
import Main from 'components/layouts/Main'
import ArticleBlog from 'components/elements/Article/Blog'

interface Props {
  query?: Query
  datas: Array<ImageResponse>
}

export default function BlogList(props: Props) {
  const {query, datas} = props
  return (
    <Main title="MyUsブログ" hero="Blog" query={query}>
      <ArticleBlog datas={datas} />
    </Main>
  )
}
