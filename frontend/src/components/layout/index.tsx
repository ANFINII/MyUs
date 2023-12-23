import { SearchTag } from 'types/internal/other'
import Header from 'components/layout/Header'
import SearchTagBar from 'components/layout/SearchTagBar'
import SideBar from 'components/layout/SideBar'

const searchtags: SearchTag[] = [
  { id: 1, name: '初音ミク' },
  { id: 2, name: 'VOCALOID' },
  { id: 3, name: '宇宙' },
]

interface Props {
  children: React.ReactNode
}

export default function Layout(props: Props) {
  const { children } = props

  return (
    <div className="layout">
      <Header />
      <SideBar />
      <SearchTagBar searchtags={searchtags} isAuth={true} />
      {children}
    </div>
  )
}
