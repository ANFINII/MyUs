import { Outlet } from '@tanstack/react-router'
import { usePageLoading } from 'components/hooks/usePageLoading'
import { useRouter } from 'components/hooks/useRouter'
import Header from 'components/layout/Header'
import SearchTagBar from 'components/layout/SearchTagBar'
import SideBar from 'components/layout/SideBar'
import { ErrorBoundary } from 'components/parts/ErrorBoundary'
import Unexpected from 'components/widgets/Status/Unexpected'
import style from './Layout.module.scss'

export default function Layout(): React.JSX.Element {
  const router = useRouter()
  const { loading } = usePageLoading()

  return (
    <div className={style.layout}>
      <Header loading={loading} />
      <SideBar />
      <SearchTagBar />
      <ErrorBoundary fallback={<Unexpected />} resetKeys={[router.pathname]}>
        <Outlet />
      </ErrorBoundary>
    </div>
  )
}
