import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { getPicture } from 'api/media'
import { Blog } from 'types/internal/media'
import BlogDetail from 'components/templates/media/blog/detail'

export const getServerSideProps: GetServerSideProps = async ({ locale, params }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const datas = await getPicture(Number(params?.id))
  return { props: { datas, ...translations } }
}

interface Props {
  datas: Blog
}

export default function BlogDetailPage(props: Props) {
  return <BlogDetail {...props} />
}
