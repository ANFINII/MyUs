import { GetStaticProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import Custom500 from 'components/widgets/Error/500'

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const translations = await serverSideTranslations(String(locale), ['common'])
  return { props: translations }
}

export default function Custom500Page(): React.JSX.Element {
  return <Custom500 />
}
