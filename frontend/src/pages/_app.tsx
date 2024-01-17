import type { AppProps } from 'next/app'
import 'styles/reset.scss'
import 'styles/global.scss'
import 'styles/layout/layout.scss'
import 'styles/layout/header.scss'
import 'styles/layout/footer.scss'
import 'styles/layout/sidebar.scss'
import 'styles/layout/searchtag.scss'
import 'styles/layout/main.scss'
import 'styles/layout/mediaquery.scss'
import 'styles/registration.scss'
import 'styles/account.scss'
import 'styles/userpolicy.scss'
import 'styles/quill.scss'
import 'styles/audio.scss'
import 'styles/videojs-myus.scss'
import { useRouter } from 'next/router'
import { AUTH_NO_PATHS } from 'lib/config'
import Layout from 'components/layout'
// import 'styles/chat.scss'

export default function MyApp({ Component, pageProps }: AppProps) {
  const router = useRouter()
  if (AUTH_NO_PATHS.includes(router.pathname)) {
    return <Component {...pageProps} />
  }

  return (
    <Layout>
      <Component {...pageProps} />
    </Layout>
  )
}
