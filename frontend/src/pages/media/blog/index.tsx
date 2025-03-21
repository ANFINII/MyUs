import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { Blog } from 'types/internal/media'
import { getBlogs } from 'api/internal/media/list'
import ErrorCheck from 'components/widgets/ErrorCheck'
import Blogs from 'components/templates/media/blog/list'

export const getServerSideProps: GetServerSideProps = async ({ locale, query }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const params = { search: String(query.search) }
  const ret = await getBlogs(params)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const datas = ret.value
  return { props: { datas, ...translations } }
}

interface Props {
  status: number
  datas: Blog[]
}

export default function BlogsPage(props: Props): JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <Blogs {...props} />
    </ErrorCheck>
  )
}
