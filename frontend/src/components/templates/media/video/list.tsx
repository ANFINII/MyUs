import { Video } from 'types/internal/media'
import { useSearch } from 'components/hooks/useSearch'
import Main from 'components/layout/Main'
import CardList from 'components/widgets/Card/List'
import VideoCard from 'components/widgets/Card/Video'

interface Props {
  datas: Video[]
}

export default function Videos(props: Props): React.JSX.Element {
  const { datas } = props

  const search = useSearch(datas)

  return (
    <Main title="Video" search={search}>
      <CardList items={datas} Content={VideoCard} />
    </Main>
  )
}
