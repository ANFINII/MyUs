import { GetStaticProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import Custom500 from 'components/templates/error/500'

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  return { props: translations }
}

export default function Custom500Page(): JSX.Element {
  return <Custom500 />
}
