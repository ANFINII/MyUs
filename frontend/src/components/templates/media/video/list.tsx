import { Video } from 'types/internal/media'
import { getVideos } from 'api/internal/media/list'
import { useNewDatas } from 'components/hooks/useNewList'
import Main from 'components/layout/Main'
import MediaList from 'components/widgets/Media/List/Media'
import MediaVideo from 'components/widgets/Media/Index/Video'

interface Props {
  datas: Video[]
}

export default function Videos(props: Props) {
  const { datas } = props

  const { search, newDatas } = useNewDatas<Video[]>({ datas, getDatas: (search) => getVideos(search) })

  return (
    <Main title="Video" search={{ name: search, count: newDatas.length }}>
      <MediaList datas={newDatas} MediaMedia={MediaVideo} />
    </Main>
  )
}
