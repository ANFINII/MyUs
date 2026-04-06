import { Video } from 'types/internal/media'
import { useSearch } from 'components/hooks/useSearch'
import Main from 'components/layout/Main'
import CardList from 'components/widgets/Card/List'
import MediaVideo from 'components/widgets/Media/Index/Video'

interface Props {
  datas: Video[]
}

export default function Videos(props: Props): React.JSX.Element {
  const { datas } = props

  const search = useSearch(datas)

  return (
    <Main title="Video" search={search}>
      <CardList cards={datas} Content={MediaVideo} />
    </Main>
  )
}
