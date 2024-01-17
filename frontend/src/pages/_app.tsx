import type { AppProps } from 'next/app'
import 'styles/reset.css'
import 'styles/global.scss'
import 'styles/layout/layout.css'
import 'styles/layout/header.css'
import 'styles/layout/footer.css'
import 'styles/layout/sidebar.css'
import 'styles/layout/searchtag.css'
import 'styles/layout/main.css'
import 'styles/layout/mediaquery.css'
import 'styles/registration.css'
import 'styles/account.css'
import 'styles/userpolicy.css'
import 'styles/quill.css'
import 'styles/audio.css'
import 'styles/videojs-myus.css'
import { useRouter } from 'next/router'
import { AUTH_NO_PATHS } from 'lib/config'
import Layout from 'components/layout'
// import 'styles/chat.css'

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
