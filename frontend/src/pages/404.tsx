import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'

export default function Custom404Page() {
  return (
    <Main title="404 Not Found">
      <h2 className="login_required">ページが見つかりませんでした!</h2>
      <Footer />
    </Main>
  )
}
