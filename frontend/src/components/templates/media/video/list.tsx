import { Video } from 'types/internal/media'
import { getVideos } from 'api/internal/media/list'
import { useNewDatas } from 'components/hooks/useNewList'
import Main from 'components/layout/Main'
import MediaVideo from 'components/widgets/Media/Index/Video'
import MediaList from 'components/widgets/Media/List/Media'

interface Props {
  datas: Video[]
}

export default function Videos(props: Props): JSX.Element {
  const { datas } = props

  const { search, newDatas } = useNewDatas<Video[]>({ datas, getDatas: (search) => getVideos(search) })

  return (
    <Main title="Video" search={{ name: search, count: newDatas.length }}>
      <MediaList medias={newDatas} MediaComponent={MediaVideo} />
    </Main>
  )
}
