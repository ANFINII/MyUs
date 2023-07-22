import { Query } from 'types/media'
import Header from 'components/layout/Header'
import Main from 'components/layout/Main'
import SearchTag from 'components/layout/SearchTag'
import SideBar from 'components/layout/SideBar'

interface searchtag {
  id: number
  name: string
}

interface Props {
  title?: string
  name?: string
  query?: Query
  header?: React.ReactNode
  sideBar?: React.ReactNode
  searchTag?: React.ReactNode
  children: React.ReactNode
}

const searchtags: searchtag[] = [
  { id: 1, name: '初音ミク' },
  { id: 2, name: 'VOCALOID' },
  { id: 3, name: '宇宙' },
]

export default function Layout(props: Props) {
  const { title, name, query } = props
  const { header, sideBar, searchTag, children } = props

  return (
    <div className="layout">
      {header || <Header />}
      {sideBar || <SideBar />}
      {searchTag || <SearchTag searchtags={searchtags} isAuthenticated={true} />}
      <Main title={title} name={name} query={query}>
        {children}
      </Main>
    </div>
  )
}
