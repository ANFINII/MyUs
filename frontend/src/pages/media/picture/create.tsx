import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import PictureCreate from 'components/templates/media/picture/create'

export const getServerSideProps: GetServerSideProps = async ({ locale }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  return { props: { ...translations } }
}

export default function PictureCreatePage(): JSX.Element {
  return <PictureCreate />
}
