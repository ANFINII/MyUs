import { Music } from 'types/internal/media'
import { useSearch } from 'components/hooks/useSearch'
import Main from 'components/layout/Main'
import MediaMusic from 'components/widgets/Media/Index/Music'
import MediaList from 'components/widgets/Media/List/Media'

interface Props {
  datas: Music[]
}

export default function Musics(props: Props): React.JSX.Element {
  const { datas } = props

  const search = useSearch(datas)

  return (
    <Main title="Music" search={search}>
      <MediaList medias={datas} MediaComponent={MediaMusic} />
    </Main>
  )
}
