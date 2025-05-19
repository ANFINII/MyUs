import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { BlogDetailOut } from 'types/internal/media'
import { getBlog } from 'api/internal/media/detail'
import ErrorCheck from 'components/widgets/Error/Check'
import BlogDetail from 'components/templates/media/blog/detail'

export const getServerSideProps: GetServerSideProps = async ({ locale, req, query }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const ret = await getBlog(Number(query.id), req)
  if (ret.isErr()) return { props: { status: ret.error.status } }
  const data = ret.value
  return { props: { data, ...translations } }
}

interface Props {
  status: number
  data: BlogDetailOut
}

export default function BlogDetailPage(props: Props): JSX.Element {
  return (
    <ErrorCheck status={props.status}>
      <BlogDetail {...props} />
    </ErrorCheck>
  )
}
