import { Picture } from 'types/internal/media'
import { useSearch } from 'components/hooks/useSearch'
import Main from 'components/layout/Main'
import CardList from 'components/widgets/Card/List'
import PictureCard from 'components/widgets/Card/Picture'

interface Props {
  datas: Picture[]
}

export default function Pictures(props: Props): React.JSX.Element {
  const { datas } = props

  const search = useSearch(datas)

  return (
    <Main title="Picture" search={search}>
      <CardList cards={datas} Content={PictureCard} />
    </Main>
  )
}
