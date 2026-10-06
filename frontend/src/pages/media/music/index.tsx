import { GetServerSideProps } from 'next'
import { Music } from 'types/internal/media/output'
import { getMusics } from 'api/internal/media/list'
import { pageParams } from 'utils/functions/common'
import ErrorCheck from 'components/widgets/Status/Check'
import Musics from 'components/templates/media/music/list'

export const getServerSideProps: GetServerSideProps = async ({ query }) => {
  const { search, limit, offset, page } = pageParams(query)
  const ret = await getMusics({ search, limit, offset })
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const { datas, total } = ret.value
  return { props: { datas, total, page } }
}

interface Props {
  status: number
  datas: Music[]
  total: number
  page: number
}

export default function MusicsPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <Musics {...props} />
    </ErrorCheck>
  )
}
