import { GetStaticProps } from 'next'
import { serverSideTranslations } from 'next-i18next/pages/serverSideTranslations'
import AdvertiseCreate from 'components/templates/manage/advertise/create'

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  return { props: { ...translations } }
}

export default function AdvertiseCreatePage(): React.JSX.Element {
  return <AdvertiseCreate />
}
