import { useLoading } from 'components/hooks/useLoading'
import Header from 'components/layout/Header'
import SearchTagBar from 'components/layout/SearchTagBar'
import SideBar from 'components/layout/SideBar'
import style from './Layout.module.scss'

interface Props {
  children: React.ReactNode
}

export default function Layout(props: Props): React.JSX.Element {
  const { children } = props

  const { loading } = useLoading()

  return (
    <div className={style.layout}>
      <Header loading={loading} />
      <SideBar />
      <SearchTagBar />
      {children}
    </div>
  )
}
