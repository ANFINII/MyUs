import { GetServerSideProps } from 'next'
import { Picture } from 'types/internal/media/output'
import { getPictures } from 'api/internal/media/list'
import { pageParams } from 'utils/functions/common'
import ErrorCheck from 'components/widgets/Status/Check'
import Pictures from 'components/templates/media/picture/list'

export const getServerSideProps: GetServerSideProps = async ({ query }) => {
  const { search, limit, offset, page } = pageParams(query)
  const ret = await getPictures({ search, limit, offset })
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const { datas, total } = ret.value
  return { props: { datas, total, page } }
}

interface Props {
  status: number
  datas: Picture[]
  total: number
  page: number
}

export default function PicturesPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <Pictures {...props} />
    </ErrorCheck>
  )
}
