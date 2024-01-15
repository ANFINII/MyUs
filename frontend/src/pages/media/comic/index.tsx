import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { getComics } from 'api/media'
import { Comic } from 'types/internal/media'
import Comics from 'components/templates/media/comic/list'

export const getServerSideProps: GetServerSideProps = async ({ locale }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const datas = getComics()
  return { props: { datas, ...translations } }
}

interface Props {
  datas: Comic[]
}

export default function ComicsPage(props: Props) {
  return <Comics {...props} />
}
