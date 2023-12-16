import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { HttpStatusCode } from 'axios'
import { apiClient } from 'lib/axios'
import { apiVideo } from 'api/uri'
import VideoDetail from 'components/templates/media/video/detail'

export const getServerSideProps: GetServerSideProps = async ({ locale, query }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const video = async (): Promise<void> => {
    await apiClient.get(apiVideo(Number(query.id))).then((res) => {
      if (res.status !== HttpStatusCode.Ok) throw Error
      res.data
    })
  }
  return { props: { video, ...translations } }
}

interface Props {
  image: string
  video: string
  publish: boolean
}

export default function VideDetailPage(props: Props) {
  return <VideoDetail {...props} />
}
