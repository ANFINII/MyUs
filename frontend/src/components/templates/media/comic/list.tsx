import { Comic } from 'types/internal/media'
import { getComics } from 'api/internal/media/list'
import { useNewDatas } from 'components/hooks/useNewList'
import Main from 'components/layout/Main'
import MediaList from 'components/widgets/Media/List/Media'
import MediaComic from 'components/widgets/Media/Index/Comic'

interface Props {
  datas: Comic[]
}

export default function Comics(props: Props) {
  const { datas } = props

  const { search, newDatas } = useNewDatas<Comic[]>({ datas, getDatas: (search) => getComics(search) })

  return (
    <Main title="Comic" search={{ name: search, count: newDatas.length }}>
      <MediaList medias={newDatas} MediaComponent={MediaComic} />
    </Main>
  )
}
