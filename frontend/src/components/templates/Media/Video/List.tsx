import { Search, VideoResponse } from 'types/media'
import Main from 'components/layout/Main'
import ArticleVideo from 'components/widgets/Article/Video'

interface Props {
  search?: Search
  datas: VideoResponse[]
}

export default function Videos(props: Props) {
  const { search, datas } = props

  return (
    <Main title="Video" search={search}>
      <article className="article_list">
        {datas.map((data) => (
          <ArticleVideo data={data} key={data.id} />
        ))}
      </article>
    </Main>
  )
}
