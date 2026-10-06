import { GetServerSideProps } from 'next'
import { VideoDetailOut } from 'types/internal/media/output'
import { getVideo } from 'api/internal/media/detail'
import ErrorCheck from 'components/widgets/Status/Check'
import VideoDetail from 'components/templates/media/video/detail'

export const getServerSideProps: GetServerSideProps = async ({ req, query }) => {
  const ret = await getVideo(String(query.ulid), req)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const data = ret.value
  return { props: { data } }
}

interface Props {
  status: number
  data: VideoDetailOut
}

export default function VideDetailPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <VideoDetail {...props} />
    </ErrorCheck>
  )
}
