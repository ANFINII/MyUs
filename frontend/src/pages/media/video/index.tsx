import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { apiClient } from 'lib/axios'
import { apiVideos } from 'api/uri'
import { Video } from 'types/internal/media'
import Videos from 'components/templates/media/video/list'

export const getServerSideProps: GetServerSideProps = async ({ locale }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const datas = await apiClient.get(apiVideos).then((res) => {
    return res.data
  })
  return { props: { datas, ...translations } }
}

interface Props {
  datas: Video[]
}

export default function VideosPage(props: Props) {
  return <Videos {...props} />
}
