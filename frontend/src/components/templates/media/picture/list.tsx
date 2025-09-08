import { Picture } from 'types/internal/media'
import { useSearch } from 'components/hooks/useSearch'
import Main from 'components/layout/Main'
import MediaPicture from 'components/widgets/Media/Index/Picture'
import MediaList from 'components/widgets/Media/List/Media'

interface Props {
  datas: Picture[]
}

export default function Pictures(props: Props): React.JSX.Element {
  const { datas } = props

  const search = useSearch(datas)

  return (
    <Main title="Picture" search={search}>
      <MediaList medias={datas} MediaComponent={MediaPicture} />
    </Main>
  )
}
