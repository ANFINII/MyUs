import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { getPictures } from 'api/media'
import { Picture } from 'types/internal/media'
import Pictures from 'components/templates/media/picture/list'

export const getServerSideProps: GetServerSideProps = async ({ locale }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const datas = getPictures()
  return { props: { datas, ...translations } }
}

interface Props {
  datas: Picture[]
}

export default function PicturesPage(props: Props) {
  return <Pictures {...props} />
}
