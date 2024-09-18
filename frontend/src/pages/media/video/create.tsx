import { GetServerSideProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import VideoCreate from 'components/templates/media/video/create'

export const getServerSideProps: GetServerSideProps = async ({ locale }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  return { props: { ...translations } }
}

export default function VideoCreatePage() {
  return <VideoCreate />
}
