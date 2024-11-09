import { Music } from 'types/internal/media'
import { getMusics } from 'api/internal/media/list'
import { useNewDatas } from 'components/hooks/useNewList'
import Main from 'components/layout/Main'
import MediaMusic from 'components/widgets/Media/Index/Music'
import MediaList from 'components/widgets/Media/List/Media'

interface Props {
  datas: Music[]
}

export default function Musics(props: Props) {
  const { datas } = props

  const { search, newDatas } = useNewDatas<Music[]>({ datas, getDatas: (search) => getMusics(search) })

  return (
    <Main title="Music" search={{ name: search, count: newDatas.length }}>
      <MediaList medias={newDatas} MediaComponent={MediaMusic} />
    </Main>
  )
}
