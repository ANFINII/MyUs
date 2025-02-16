import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { Picture } from 'types/internal/media'
import { getPictures } from 'api/internal/media/list'
import Pictures from 'components/templates/media/picture/list'

export const getServerSideProps: GetServerSideProps = async ({ locale, query }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const params = { search: String(query.search) }
  const datas = await getPictures(params)
  return { props: { datas, ...translations } }
}

interface Props {
  datas: Picture[]
}

export default function PicturesPage(props: Props): JSX.Element {
  return <Pictures {...props} />
}
