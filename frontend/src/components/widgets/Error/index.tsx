import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import BackError from 'components/parts/Error/Back'

export default function Error(): React.JSX.Element {
  return (
    <Main title="Unexpected Error">
      <BackError content="予期せぬエラーが発生しました" />
      <Footer />
    </Main>
  )
}
