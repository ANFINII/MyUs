import Head from 'next/head'
import Footer from 'components/layouts/footer'

export default function Custom404() {
  return (
    <article className="article_pass">
      <Head>
        <title>MyUs404</title>
      </Head>

      <h1>404 Not Found</h1>
      <h2 className="login_required">ページが見つかりませんでした!</h2>

      <Footer/>
    </article>
  )
}
