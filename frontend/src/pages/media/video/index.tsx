import { GetServerSideProps } from 'next'
import { Video } from 'types/internal/media/output'
import { getVideos } from 'api/internal/media/list'
import { pageParams } from 'utils/functions/common'
import ErrorCheck from 'components/widgets/Status/Check'
import Videos from 'components/templates/media/video/list'

export const getServerSideProps: GetServerSideProps = async ({ query }) => {
  const { search, limit, offset, page } = pageParams(query)
  const ret = await getVideos({ search, limit, offset })
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const { datas, total } = ret.value
  return { props: { datas, total, page } }
}

interface Props {
  status: number
  datas: Video[]
  total: number
  page: number
}

export default function VideosPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <Videos {...props} />
    </ErrorCheck>
  )
}
