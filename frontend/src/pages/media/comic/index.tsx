import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { Comic } from 'types/internal/media/output'
import { getComics } from 'api/internal/media/list'
import { pageParams } from 'utils/functions/common'
import ErrorCheck from 'components/widgets/Error/Check'
import Comics from 'components/templates/media/comic/list'

export const getServerSideProps: GetServerSideProps = async ({ locale, query }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const { search, limit, offset, page } = pageParams(query)
  const ret = await getComics({ search, limit, offset })
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const { datas, total } = ret.value
  return { props: { ...translations, datas, total, page } }
}

interface Props {
  status: number
  datas: Comic[]
  total: number
  page: number
}

export default function ComicsPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <Comics {...props} />
    </ErrorCheck>
  )
}
