import type { AppProps } from 'next/app'
import { useRouter } from 'next/router'
import { appWithTranslation } from 'next-i18next'
import { UserProvider } from 'components/provider/UserProvider'
import Layout from 'components/layout'
import { ErrorBoundary } from 'components/parts/ErrorBoundary'
import Unexpected from 'components/widgets/Error/Unexpected'
import 'video.js/dist/video-js.css'
import 'styles/global/reset.scss'
import 'styles/global/style.scss'
import 'styles/global/index.scss'
import 'styles/global/main_other.scss'
import 'styles/internal/account.scss'
import 'styles/internal/userpolicy.scss'
import 'styles/internal/registration.scss'
import 'styles/internal/videojs-myus.scss'

function MyApp(props: AppProps) {
  const { Component, pageProps } = props
  const router = useRouter()
  return (
    <UserProvider>
      <Layout>
        <ErrorBoundary fallback={<Unexpected />} resetKeys={[router.pathname]}>
          <Component {...pageProps} />
        </ErrorBoundary>
      </Layout>
    </UserProvider>
  )
}

export default appWithTranslation(MyApp)
