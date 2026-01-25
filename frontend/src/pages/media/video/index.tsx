import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { Video } from 'types/internal/media'
import { getVideos } from 'api/internal/media/list'
import { searchParams } from 'utils/functions/common'
import ErrorCheck from 'components/widgets/Error/Check'
import Videos from 'components/templates/media/video/list'

export const getServerSideProps: GetServerSideProps = async ({ locale, query }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const params = searchParams(query)
  const ret = await getVideos(params)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const datas = ret.value
  return { props: { ...translations, datas } }
}

interface Props {
  status: number
  datas: Video[]
}

export default function VideosPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <Videos {...props} />
    </ErrorCheck>
  )
}
