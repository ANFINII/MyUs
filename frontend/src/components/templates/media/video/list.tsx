import { getVideos } from 'api/internal/media/list'
import { Video } from 'types/internal/media'
import { useNewDatas } from 'components/hooks/useNewList'
import Main from 'components/layout/Main'
import ArticleVideo from 'components/widgets/Article/Video'

interface Props {
  datas: Video[]
}

export default function Videos(props: Props) {
  const { datas } = props

  const { search, newDatas } = useNewDatas<Video[]>({ datas, getDatas: (search) => getVideos(search) })

  return (
    <Main title="Video" search={{ name: search, count: newDatas.length }}>
      <article className="article_list">
        {newDatas.map((data) => (
          <ArticleVideo key={data.id} data={data} />
        ))}
      </article>
    </Main>
  )
}
