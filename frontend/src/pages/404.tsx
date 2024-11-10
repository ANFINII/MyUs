import { GetStaticProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import Custom404 from 'components/templates/error/404'

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  return { props: translations }
}

export default function Custom404Page() {
  return <Custom404 />
}
