import { MediaHome } from 'types/internal/media/output'
import { mediaCount } from 'utils/functions/common'
import { useSearch } from 'components/hooks/useSearch'
import Main from 'components/layout/Main'
import Divide from 'components/parts/Divide'
import MediaIndexList from 'components/widgets/Card/MediaIndexList'

interface Props {
  title: string
  data: MediaHome
}

export default function Homes(props: Props): React.JSX.Element {
  const { title, data } = props

  const search = useSearch(mediaCount(data))

  return (
    <Main title={title} search={search}>
      <Divide />
      <MediaIndexList media={data} />
    </Main>
  )
}
