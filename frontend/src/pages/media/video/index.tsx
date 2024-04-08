import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { getVideos } from 'api/media/get/list'
import { Video } from 'types/internal/media'
import Videos from 'components/templates/media/video/list'

export const getServerSideProps: GetServerSideProps = async ({ locale }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const datas = await getVideos()
  return { props: { datas, ...translations } }
}

interface Props {
  datas: Video[]
}

export default function VideosPage(props: Props) {
  return <Videos {...props} />
}
