import Layout from 'components/layout'
import Footer from 'components/layout/Footer'

export default function Custom500Page() {
  return (
    <Layout title="500 Server Error">
      <h2 className="login_required">このページは動作しませんでした!</h2>
      <Footer />
    </Layout>
  )
}
