import { useLoading } from 'components/hooks/useLoading'
import Header from 'components/layout/Header'
import SearchTagBar from 'components/layout/SearchTagBar'
import SideBar from 'components/layout/SideBar'

interface Props {
  children: React.ReactNode
}

export default function Layout(props: Props): JSX.Element {
  const { children } = props

  const { loading } = useLoading()

  return (
    <div className="layout">
      <Header loading={loading} />
      <SideBar />
      <SearchTagBar />
      {children}
    </div>
  )
}
