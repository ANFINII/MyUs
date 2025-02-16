import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { Video } from 'types/internal/media'
import { getVideos } from 'api/internal/media/list'
import Videos from 'components/templates/media/video/list'

export const getServerSideProps: GetServerSideProps = async ({ locale, query }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const params = { search: String(query.search) }
  const datas = await getVideos(params)
  return { props: { datas, ...translations } }
}

interface Props {
  datas: Video[]
}

export default function VideosPage(props: Props): JSX.Element {
  return <Videos {...props} />
}
