import { Search } from 'types/media'
import Meta from 'components/layout/Head/Meta'
import Header from 'components/layout/Header'
import Main from 'components/layout/Main'
import SearchTag from 'components/layout/SearchTag'
import SideBar from 'components/layout/SideBar'

interface searchtag {
  id: number
  name: string
}

interface Props {
  title: string
  search?: Search
  children: React.ReactNode
}

const searchtags: searchtag[] = [
  { id: 1, name: '初音ミク' },
  { id: 2, name: 'VOCALOID' },
  { id: 3, name: '宇宙' },
]

export default function Layout(props: Props) {
  const { title, search, children } = props

  return (
    <div className="layout">
      {<Header />}
      {<SideBar />}
      {<SearchTag searchtags={searchtags} isAuthenticated={true} />}
      <Meta title={title} />
      <Main title={title} search={search}>
        {children}
      </Main>
    </div>
  )
}
