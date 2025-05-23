import type { AppProps } from 'next/app'
import { useRouter } from 'next/router'
import { UserProvider } from 'components/provider/UserProvider'
import Layout from 'components/layout'
import { ErrorBoundary } from 'components/parts/ErrorBoundary'
import Error from 'components/widgets/Error'
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
  const router = useRouter()
  return (
    <UserProvider>
      <Layout>
        <ErrorBoundary fallback={<Error />} resetKeys={[router.pathname]}>
          <Component {...pageProps} />
        </ErrorBoundary>
      </Layout>
    </UserProvider>
  )
}
