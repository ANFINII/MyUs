import { GetServerSideProps } from 'next'
import { MediaHome } from 'types/internal/media/output'
import { getHome } from 'api/internal/media/list'
import { searchParams } from 'utils/functions/common'
import ErrorCheck from 'components/widgets/Status/Check'
import Homes from 'components/templates/media/home/list'

export const getServerSideProps: GetServerSideProps = async ({ query }) => {
  const params = searchParams(query)
  const ret = await getHome(params)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const mediaHome = ret.value
  return { props: { mediaHome } }
}

interface Props {
  status: number
  mediaHome: MediaHome
}

export default function HomesPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <Homes title="Home" {...props} />
    </ErrorCheck>
  )
}
