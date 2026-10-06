import { createRootRoute, Outlet } from '@tanstack/react-router'
import { useAppRouter } from 'components/hooks/useAppRouter'
import Layout from 'components/layout'
import { ErrorBoundary } from 'components/parts/ErrorBoundary'
import Unexpected from 'components/widgets/Status/Unexpected'

function RootLayout(): React.JSX.Element {
  const router = useAppRouter()

  return (
    <Layout>
      <ErrorBoundary fallback={<Unexpected />} resetKeys={[router.pathname]}>
        <Outlet />
      </ErrorBoundary>
    </Layout>
  )
}

export const Route = createRootRoute({ component: RootLayout })
