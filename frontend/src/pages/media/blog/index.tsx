import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { getBlogs } from 'api/media/get'
import { Blog } from 'types/internal/media'
import Blogs from 'components/templates/media/blog/list'

export const getServerSideProps: GetServerSideProps = async ({ locale }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const datas = await getBlogs()
  return { props: { datas, ...translations } }
}

interface Props {
  datas: Blog[]
}

export default function BlogsPage(props: Props) {
  return <Blogs {...props} />
}
