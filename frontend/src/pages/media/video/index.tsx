import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { Video } from 'types/internal/media'
import { getVideos } from 'api/internal/media/list'
import ErrorCheck from 'components/widgets/ErrorCheck'
import Videos from 'components/templates/media/video/list'

export const getServerSideProps: GetServerSideProps = async ({ locale, query }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const params = { search: String(query.search) }
  const ret = await getVideos(params)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const datas = ret.value
  return { props: { datas, ...translations } }
}

interface Props {
  status: number
  datas: Video[]
}

export default function VideosPage(props: Props): JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <Videos {...props} />
    </ErrorCheck>
  )
}
