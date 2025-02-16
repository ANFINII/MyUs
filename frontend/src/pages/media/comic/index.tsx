import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { Comic } from 'types/internal/media'
import { getComics } from 'api/internal/media/list'
import Comics from 'components/templates/media/comic/list'

export const getServerSideProps: GetServerSideProps = async ({ locale, query }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const params = { search: String(query.search) }
  const datas = await getComics(params)
  return { props: { datas, ...translations } }
}

interface Props {
  datas: Comic[]
}

export default function ComicsPage(props: Props): JSX.Element {
  return <Comics {...props} />
}
