import { GetServerSideProps } from 'next'
import { ComicDetailOut } from 'types/internal/media/output'
import { getComic } from 'api/internal/media/detail'
import ErrorCheck from 'components/widgets/Status/Check'
import ComicDetail from 'components/templates/media/comic/detail'

export const getServerSideProps: GetServerSideProps = async ({ req, query }) => {
  const ret = await getComic(String(query.ulid), req)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const data = ret.value
  return { props: { data } }
}

interface Props {
  status: number
  data: ComicDetailOut
}

export default function ComicDetailPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <ComicDetail {...props} />
    </ErrorCheck>
  )
}
