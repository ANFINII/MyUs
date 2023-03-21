import Head from 'next/head'
import Footer from 'components/layouts/Footer'

export default function Custom500() {
  return (
    <article className="article_pass">
      <Head>
        <title>MyUs500</title>
      </Head>

      <h1>500 Server Error</h1>
      <h2 className="login_required">このページは動作しませんでした!</h2>

      <Footer />
    </article>
  )
}
