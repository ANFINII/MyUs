import { Music } from 'types/internal/media'
import { useSearch } from 'components/hooks/useSearch'
import Main from 'components/layout/Main'
import CardList from 'components/widgets/Card/List'
import MusicCard from 'components/widgets/Card/Media/Music'

interface Props {
  datas: Music[]
}

export default function Musics(props: Props): React.JSX.Element {
  const { datas } = props

  const search = useSearch(datas)

  return (
    <Main title="Music" search={search}>
      <CardList items={datas} Content={MusicCard} />
    </Main>
  )
}
