import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import BackError from 'components/parts/Error/Back'

export default function Custom500(): JSX.Element {
  return (
    <Main title="500 Server Error">
      <BackError content="このページは動作しませんでした" />
      <Footer />
    </Main>
  )
}
