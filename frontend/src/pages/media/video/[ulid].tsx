import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { VideoDetailOut } from 'types/internal/media/detail'
import { getVideo } from 'api/internal/media/detail'
import ErrorCheck from 'components/widgets/Error/Check'
import VideoDetail from 'components/templates/media/video/detail'

export const getServerSideProps: GetServerSideProps = async ({ locale, req, query }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const ret = await getVideo(String(query.ulid), req)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const data = ret.value
  return { props: { ...translations, data } }
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
