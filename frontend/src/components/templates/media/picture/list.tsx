import { Picture } from 'types/internal/media'
import { getPictures } from 'api/internal/media/list'
import { useNewDatas } from 'components/hooks/useNewList'
import Main from 'components/layout/Main'
import MediaList from 'components/widgets/Media/List/Media'
import MediaPicture from 'components/widgets/Media/Index/Picture'

interface Props {
  datas: Picture[]
}

export default function Pictures(props: Props) {
  const { datas } = props

  const { search, newDatas } = useNewDatas<Picture[]>({ datas, getDatas: (search) => getPictures(search) })

  return (
    <Main title="Picture" search={{ name: search, count: newDatas.length }}>
      <MediaList datas={newDatas} MediaMedia={MediaPicture} />
    </Main>
  )
}
