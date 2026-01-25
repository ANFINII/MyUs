import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import BackError from 'components/parts/Error/Back'

export default function Unauthorized(): React.JSX.Element {
  return (
    <Main title="Unauthorized">
      <BackError content="ログインしてください" />
      <Footer />
    </Main>
  )
}
