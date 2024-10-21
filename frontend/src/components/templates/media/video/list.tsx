import { getVideos } from 'api/internal/media/list'
import { Video } from 'types/internal/media'
import { useNewDatas } from 'components/hooks/useNewList'
import Main from 'components/layout/Main'
import ArticleMedia from 'components/widgets/Media/Article/Media'
import SectionVideo from 'components/widgets/Media/Section/Video'

interface Props {
  datas: Video[]
}

export default function Videos(props: Props) {
  const { datas } = props

  const { search, newDatas } = useNewDatas<Video[]>({ datas, getDatas: (search) => getVideos(search) })

  return (
    <Main title="Video" search={{ name: search, count: newDatas.length }}>
      <ArticleMedia datas={newDatas} SectionMedia={SectionVideo} />
    </Main>
  )
}
