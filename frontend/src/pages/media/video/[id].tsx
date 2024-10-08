import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { getServerVideo } from 'api/internal/media/detail'
import { Video } from 'types/internal/media'
import VideoDetail from 'components/templates/media/video/detail'

export const getServerSideProps: GetServerSideProps = async ({ locale, req, query }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const video = await getServerVideo(req, Number(query?.id))
  return { props: { video, ...translations } }
}

interface Props {
  video: Video
}

export default function VideDetailPage(props: Props) {
  return <VideoDetail {...props} />
}
