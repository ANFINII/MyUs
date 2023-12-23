import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'

export default function Custom500Page() {
  return (
    <Main title="500 Server Error">
      <h2 className="login_required">このページは動作しませんでした!</h2>
      <Footer />
    </Main>
  )
}
