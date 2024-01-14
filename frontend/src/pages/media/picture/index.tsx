import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import { apiClient } from 'lib/axios'
import { apiPictures } from 'api/uri'
import { Picture } from 'types/internal/media'
import Pictures from 'components/templates/media/picture/list'

export const getServerSideProps: GetServerSideProps = async ({ locale }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  const datas = await apiClient.get(apiPictures).then((res) => {
    return res.data
  })
  return { props: { datas, ...translations } }
}

interface Props {
  datas: Picture[]
}

export default function PicturesPage(props: Props) {
  return <Pictures {...props} />
}
