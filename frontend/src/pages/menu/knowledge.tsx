import { GetStaticProps } from 'next'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import Knowledge from 'components/templates/menu/knowledge'

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  return { props: translations }
}

export default function KnowledgePage(): JSX.Element {
  return <Knowledge />
}
