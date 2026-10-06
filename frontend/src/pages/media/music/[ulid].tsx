import { GetServerSideProps } from 'next'
import { MusicDetailOut } from 'types/internal/media/output'
import { getMusic } from 'api/internal/media/detail'
import ErrorCheck from 'components/widgets/Status/Check'
import MusicDetail from 'components/templates/media/music/detail'

export const getServerSideProps: GetServerSideProps = async ({ req, query }) => {
  const ret = await getMusic(String(query.ulid), req)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const data = ret.value
  return { props: { data } }
}

interface Props {
  status: number
  data: MusicDetailOut
}

export default function MusicDetailPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <MusicDetail {...props} />
    </ErrorCheck>
  )
}
