import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { apiClient } from 'lib/axios'
import { apiHome } from 'api/uri'
import { HomeMedia } from 'types/internal/media'
import Homes from 'components/templates/media/home/list'

export const getServerSideProps: GetServerSideProps = async ({ locale }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const homeMedia = await apiClient.get(apiHome).then((res) => {
    return res.data
  })
  return { props: { homeMedia, ...translations } }
}

interface Props {
  homeMedia: HomeMedia
}

export default function HomesPage(props: Props) {
  return <Homes {...props} />
}
