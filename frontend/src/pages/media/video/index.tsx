import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { Video } from 'types/internal/media/output'
import { getVideos } from 'api/internal/media/list'
import { pageParams } from 'utils/functions/common'
import ErrorCheck from 'components/widgets/Error/Check'
import Videos from 'components/templates/media/video/list'

export const getServerSideProps: GetServerSideProps = async ({ locale, query }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const { search, limit, offset, page } = pageParams(query)
  const ret = await getVideos({ search, limit, offset })
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const { datas, total } = ret.value
  return { props: { ...translations, datas, total, page } }
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
