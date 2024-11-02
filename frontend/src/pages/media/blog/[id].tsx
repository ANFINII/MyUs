import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { BlogDetailOut } from 'types/internal/media'
import { getBlog } from 'api/internal/media/detail'
import BlogDetail from 'components/templates/media/blog/detail'

export const getServerSideProps: GetServerSideProps = async ({ locale, req, query }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const data = await getBlog(Number(query.id), req)
  return { props: { data, ...translations } }
}

interface Props {
  data: BlogDetailOut
}

export default function BlogDetailPage(props: Props) {
  return <BlogDetail {...props} />
}
