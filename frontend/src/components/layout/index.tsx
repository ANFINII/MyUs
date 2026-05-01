import { usePageLoading } from 'components/hooks/usePageLoading'
import Header from 'components/layout/Header'
import SearchTagBar from 'components/layout/SearchTagBar'
import SideBar from 'components/layout/SideBar'
import style from './Layout.module.scss'

interface Props {
  children: React.ReactNode
}

export default function Layout(props: Props): React.JSX.Element {
  const { children } = props

  const { loading } = usePageLoading()

  return (
    <div className={style.layout}>
      <Header loading={loading} />
      <SideBar />
      <SearchTagBar />
      {children}
    </div>
  )
}
