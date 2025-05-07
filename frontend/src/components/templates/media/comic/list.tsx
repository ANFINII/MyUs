import { Comic } from 'types/internal/media'
import { useSearch } from 'components/hooks/useSearch'
import Main from 'components/layout/Main'
import MediaComic from 'components/widgets/Media/Index/Comic'
import MediaList from 'components/widgets/Media/List/Media'

interface Props {
  datas: Comic[]
}

export default function Comics(props: Props): JSX.Element {
  const { datas } = props

  const search = useSearch(datas)

  return (
    <Main title="Comic" search={search}>
      <MediaList medias={datas} MediaComponent={MediaComic} />
    </Main>
  )
}
