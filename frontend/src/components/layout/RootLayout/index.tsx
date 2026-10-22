import { Outlet } from '@tanstack/react-router'
import { useRouter } from 'components/hooks/useRouter'
import Layout from 'components/layout'
import { ErrorBoundary } from 'components/parts/ErrorBoundary'
import Unexpected from 'components/widgets/Status/Unexpected'

export default function RootLayout(): React.JSX.Element {
  const router = useRouter()

  return (
    <Layout>
      <ErrorBoundary fallback={<Unexpected />} resetKeys={[router.pathname]}>
        <Outlet />
      </ErrorBoundary>
    </Layout>
  )
}
