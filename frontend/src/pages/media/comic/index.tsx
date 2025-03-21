import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { Comic } from 'types/internal/media'
import { getComics } from 'api/internal/media/list'
import ErrorCheck from 'components/widgets/ErrorCheck'
import Comics from 'components/templates/media/comic/list'

export const getServerSideProps: GetServerSideProps = async ({ locale, query }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const params = { search: String(query.search) }
  const ret = await getComics(params)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const datas = ret.value
  return { props: { datas, ...translations } }
}

interface Props {
  status: number
  datas: Comic[]
}

export default function ComicsPage(props: Props): JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <Comics {...props} />
    </ErrorCheck>
  )
}
