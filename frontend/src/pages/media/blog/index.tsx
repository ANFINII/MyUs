import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { getPictures } from 'api/media'
import { Picture } from 'types/internal/media'
import Blogs from 'components/templates/media/blog/list'

export const getServerSideProps: GetServerSideProps = async ({ locale }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const datas = await getPictures()
  return { props: { datas, ...translations } }
}

interface Props {
  datas: Picture[]
}

export default function BlogsPage(props: Props) {
  return <Blogs {...props} />
}
