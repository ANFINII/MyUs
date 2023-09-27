import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import config from 'api/config'
import { GetStaticPathsType } from 'types/global/next'
import { Video } from 'types/internal/media'
import VideoDetail from 'components/templates/media/video/detail'

export async function getStaticPaths(): Promise<GetStaticPathsType> {
  const url = config.baseUrl + '/media/video'
  const res = await fetch(config.baseUrl + url)
  const videos: Video[] = await res.json()
  const paths = videos.map((video) => ({
    params: { id: String(video.id) },
  }))
  return { paths, fallback: 'blocking' }
}

export const getServerSideProps: GetServerSideProps = async ({ locale, params }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const res = await fetch(config.baseUrl + `/api//media/video/detail/${params?.id}`)
  if (res.status !== 200) throw Error
  const data = await res.json()
  return { props: { data, translations } }
}

interface Props {
  image: string
  video: string
  publish: boolean
}

export default function VideDetailPage(props: Props) {
  const { image, video, publish } = props
  return <VideoDetail image={image} video={video} publish={publish} />
}
