import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { Video } from 'types/internal/media'
import { getVideo } from 'api/internal/media/detail'
import VideoDetail from 'components/templates/media/video/detail'

export const getServerSideProps: GetServerSideProps = async ({ locale, req, query }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const video = await getVideo(Number(query?.id), req)
  return { props: { video, ...translations } }
}

interface Props {
  video: Video
}

export default function VideDetailPage(props: Props): JSX.Element {
  return <VideoDetail {...props} />
}
