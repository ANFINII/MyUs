import { GetStaticProps } from 'next'
import { useRouter } from 'next/router'
import { serverSideTranslations } from 'next-i18next/serverSideTranslations'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const translations = await serverSideTranslations(locale as string, ['common'])
  return { props: translations }
}

export default function Custom404Page() {
  const router = useRouter()

  return (
    <Main title="404 Not Found">
      <h2 className="login_required mt_20">ページが見つかりませんでした</h2>
      <Button name="戻る" className="mt_24 w_80" onClick={() => router.back()} />
      <Footer />
    </Main>
  )
}
