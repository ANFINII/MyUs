import type { AppProps } from 'next/app'
import { UserProvider } from 'components/provider/UserProvider'
import Layout from 'components/layout'
import 'styles/global/reset.scss'
import 'styles/global/style.scss'
import 'styles/global/quill/index.scss'
import 'styles/global/quill/blog.scss'
import 'styles/layout/index.scss'
import 'styles/layout/header.scss'
import 'styles/layout/footer.scss'
import 'styles/layout/sidebar.scss'
import 'styles/layout/searchtag.scss'
import 'styles/layout/main.scss'
import 'styles/layout/main_other.scss'
import 'styles/layout/mediaquery.scss'
import 'styles/internal/account.scss'
import 'styles/internal/userpolicy.scss'
import 'styles/internal/registration.scss'
import 'styles/internal/audio.scss'
import 'styles/internal/videojs-myus.scss'

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <UserProvider>
      <Layout>
        <Component {...pageProps} />
      </Layout>
    </UserProvider>
  )
}
