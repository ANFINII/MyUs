import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import BackError from 'components/parts/Error/Back'

export default function Custom404(): JSX.Element {
  return (
    <Main title="404 Not Found">
      <BackError content="ページが見つかりませんでした" />
      <Footer />
    </Main>
  )
}
