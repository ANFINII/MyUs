import { Video } from 'types/internal/media'
import { useSearch } from 'components/hooks/useSearch'
import Main from 'components/layout/Main'
import MediaVideo from 'components/widgets/Media/Index/Video'
import MediaList from 'components/widgets/Media/List/Media'

interface Props {
  datas: Video[]
}

export default function Videos(props: Props): JSX.Element {
  const { datas } = props

  const search = useSearch(datas)

  return (
    <Main title="Video" search={search}>
      <MediaList medias={datas} MediaComponent={MediaVideo} />
    </Main>
  )
}
