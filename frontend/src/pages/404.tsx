import Layout from 'components/layout'
import Footer from 'components/layout/Footer'

export default function Custom404() {
  return (
    <Layout title="404 Not Found">
      <h2 className="login_required">ページが見つかりませんでした!</h2>
      <Footer />
    </Layout>
  )
}
