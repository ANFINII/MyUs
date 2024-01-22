import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { getHome } from 'api/media'
import { MediaHome } from 'types/internal/media'
import Homes from 'components/templates/media/home/list'

export const getServerSideProps: GetServerSideProps = async ({ locale }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const mediaHome = await getHome()
  return { props: { mediaHome, ...translations } }
}

interface Props {
  mediaHome: MediaHome
}

export default function HomesPage(props: Props) {
  return <Homes {...props} />
}
