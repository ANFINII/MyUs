import { Music } from 'types/internal/media'
import { useSearch } from 'components/hooks/useSearch'
import Main from 'components/layout/Main'
import CardList from 'components/widgets/Card/List'
import MediaMusic from 'components/widgets/Card/Music'

interface Props {
  datas: Music[]
}

export default function Musics(props: Props): React.JSX.Element {
  const { datas } = props

  const search = useSearch(datas)

  return (
    <Main title="Music" search={search}>
      <CardList cards={datas} Content={MediaMusic} />
    </Main>
  )
}
