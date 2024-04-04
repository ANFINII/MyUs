import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { getBlog } from 'api/media/get'
import { Blog } from 'types/internal/media'
import BlogDetail from 'components/templates/media/blog/detail'

export const getServerSideProps: GetServerSideProps = async ({ locale, req, query }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const data = await getBlog(Number(query.id))
  return { props: { data, ...translations } }
}

interface Props {
  data: Blog
}

export default function BlogDetailPage(props: Props) {
  return <BlogDetail {...props} />
}
