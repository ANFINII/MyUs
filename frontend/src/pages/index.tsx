import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { apiClient } from 'lib/axios'
import { apiHome } from 'api/uri'
import { HomeMedia, Search } from 'types/internal/media'
import Homes from 'components/templates/media/home/list'

export const getServerSideProps: GetServerSideProps = async ({ locale }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const homeMedia = async () => {
    await apiClient.get(apiHome).then((res) => {
      res.data
    })
  }
  return { props: { homeMedia, ...translations } }
}

interface Props {
  homeMedia: HomeMedia
  search?: Search
}

export default function HomesPage(props: Props) {
  return <Homes {...props} />
}

// {
//   /* <Script src="https://vjs.zencdn.net/7.19.2/video.min.js"></Script>
// <Script src='/pages/api/video_auto.js'></Script>
// <script>$(function() { $('audio').audioPlayer() })</cript> */
// }
