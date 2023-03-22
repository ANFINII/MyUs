import {Query, VideoResponse} from 'utils/type'
import Main from 'components/layouts/Main'
import ArticleVideo from 'components/elements/Article/Video'

interface Props {
  query?: Query
  datas: Array<VideoResponse>
}

export default function VideoList(props: Props) {
  const {query, datas} = props
  return (
    <Main title="MyUsビデオ" hero="Video" query={query}>
      <ArticleVideo datas={datas} />
    </Main>
  )
}
