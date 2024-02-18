import type { AppProps } from 'next/app'
import 'styles/reset.scss'
import 'styles/layout/index.scss'
import 'styles/layout/header.scss'
import 'styles/layout/footer.scss'
import 'styles/layout/sidebar.scss'
import 'styles/layout/searchtag.scss'
import 'styles/layout/main.scss'
import 'styles/layout/mediaquery.scss'
import 'styles/global/index.scss'
import 'styles/global/account.scss'
import 'styles/global/userpolicy.scss'
import 'styles/global/registration.scss'
import 'styles/global/quill/index.scss'
import 'styles/global/quill/blog.scss'
import 'styles/global/audio.scss'
import 'styles/global/videojs-myus.scss'
import Layout from 'components/layout'

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <Layout>
      <Component {...pageProps} />
    </Layout>
  )
}
