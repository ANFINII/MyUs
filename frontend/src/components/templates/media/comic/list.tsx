import { Comic } from 'types/internal/media'
import { useSearch } from 'components/hooks/useSearch'
import Main from 'components/layout/Main'
import CardList from 'components/widgets/Card/List'
import ComicCard from 'components/widgets/Card/Media/Comic'

interface Props {
  datas: Comic[]
}

export default function Comics(props: Props): React.JSX.Element {
  const { datas } = props

  const search = useSearch(datas)

  return (
    <Main title="Comic" search={search}>
      <CardList items={datas} Content={ComicCard} />
    </Main>
  )
}
