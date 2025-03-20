import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import BackError from 'components/parts/Error/Back'

export default function Error(): JSX.Element {
  return (
    <Main title="Front End Error">
      <BackError content="UIでエラーが発生しました" />
      <Footer />
    </Main>
  )
}
