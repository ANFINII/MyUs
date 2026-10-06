import type { AppProps } from 'next/app'
import { useAppRouter } from 'components/hooks/useAppRouter'
import { AppProvider } from 'components/provider/AppProvider'
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
    <AppProvider>
      <Layout>
        <ErrorBoundary fallback={<Unexpected />} resetKeys={[router.pathname]}>
          <Component {...pageProps} />
        </ErrorBoundary>
      </Layout>
    </AppProvider>
  )
}

export default MyApp
