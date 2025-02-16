import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { Blog } from 'types/internal/media'
import { getBlogs } from 'api/internal/media/list'
import Blogs from 'components/templates/media/blog/list'

export const getServerSideProps: GetServerSideProps = async ({ locale, query }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const params = { search: String(query.search) }
  const datas = await getBlogs(params)
  return { props: { datas, ...translations } }
}

interface Props {
  datas: Blog[]
}

export default function BlogsPage(props: Props): JSX.Element {
  return <Blogs {...props} />
}
