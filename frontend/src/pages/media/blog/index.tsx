import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import { Blog } from 'types/internal/media/output'
import { getBlogs } from 'api/internal/media/list'
import { pageParams } from 'utils/functions/common'
import ErrorCheck from 'components/widgets/Error/Check'
import Blogs from 'components/templates/media/blog/list'

export const getServerSideProps: GetServerSideProps = async ({ locale, query }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  const { search, limit, offset, page } = pageParams(query)
  const ret = await getBlogs({ search, limit, offset })
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const { datas, total } = ret.value
  return { props: { ...translations, datas, total, page } }
}

interface Props {
  status: number
  datas: Blog[]
  total: number
  page: number
}

export default function BlogsPage(props: Props): React.JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <Blogs {...props} />
    </ErrorCheck>
  )
}
