import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import BackLogin from 'components/parts/Error/Login'

export default function Unauthorized(): React.JSX.Element {
  return (
    <Main title="Unauthorized">
      <BackLogin content="ログインしてください" />
      <Footer />
    </Main>
  )
}
