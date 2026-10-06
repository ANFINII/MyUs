import type { AppProps } from 'next/app'
import { useAppRouter } from 'components/hooks/useAppRouter'
import { I18nProvider } from 'components/provider/I18nProvider'
import { QueryProvider } from 'components/provider/QueryProvider'
import { UserProvider } from 'components/provider/UserProvider'
import Layout from 'components/layout'
import { ErrorBoundary } from 'components/parts/ErrorBoundary'
import Unexpected from 'components/widgets/Status/Unexpected'
import 'video.js/dist/video-js.css'
import 'styles/global/reset.scss'
import 'styles/global/style.scss'
import 'styles/global/index.scss'
import 'styles/global/main_other.scss'
import 'styles/internal/userpolicy.scss'
import 'styles/internal/registration.scss'
import 'styles/internal/videojs-myus.scss'

function MyApp(props: AppProps) {
  const { Component, pageProps } = props
  const router = useAppRouter()
  return (
    <I18nProvider>
      <QueryProvider>
        <UserProvider>
          <Layout>
            <ErrorBoundary fallback={<Unexpected />} resetKeys={[router.pathname]}>
              <Component {...pageProps} />
            </ErrorBoundary>
          </Layout>
        </UserProvider>
      </QueryProvider>
    </I18nProvider>
  )
}

export default MyApp
