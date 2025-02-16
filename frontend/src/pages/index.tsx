import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { MediaHome } from 'types/internal/media'
import { getHome } from 'api/internal/media/list'
import Homes from 'components/templates/media/home/list'

export const getServerSideProps: GetServerSideProps = async ({ locale, query }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const params = { search: String(query.search) }
  const mediaHome = await getHome(params)
  return { props: { mediaHome, ...translations } }
}

interface Props {
  mediaHome: MediaHome
}

export default function HomesPage(props: Props): JSX.Element {
  return <Homes {...props} />
}
