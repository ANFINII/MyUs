import 'bootstrap/dist/css/bootstrap.min.css';
// import 'bootstrap-icons/font/bootstrap-icons.css';
import 'styles/bootstrap.css'
import 'styles/globals.css'
import 'styles/index.css'
import 'styles/profile.css'
import 'styles/userpolicy.css'
import type { AppProps } from 'next/app'
import Layout from 'components/layouts/layout'

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <Layout>
      <Component {...pageProps}/>
    </Layout>
  )
}

export default MyApp
