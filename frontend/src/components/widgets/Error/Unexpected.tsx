import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import BackError from 'components/parts/Error/Back'

export default function Unexpected(): React.JSX.Element {
  return (
    <Main title="Unexpected Error">
      <BackError content="予期せぬエラーが発生しました" />
      <Footer />
    </Main>
  )
}
