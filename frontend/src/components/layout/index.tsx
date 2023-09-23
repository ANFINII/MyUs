import { Search } from 'types/media'
import { searchtag } from 'types/other'
import Footer from 'components/layout/Footer'
import Meta from 'components/layout/Head/Meta'
import Header from 'components/layout/Header'
import Main from 'components/layout/Main'
import SearchTag from 'components/layout/SearchTag'
import SideBar from 'components/layout/SideBar'

const searchtags: searchtag[] = [
  { id: 1, name: '初音ミク' },
  { id: 2, name: 'VOCALOID' },
  { id: 3, name: '宇宙' },
]

interface Props {
  title?: string
  search?: Search
  type?: 'defalt' | 'table'
  isFooter?: boolean
  children: React.ReactNode
}

export default function Layout(props: Props) {
  const { title, search, type = 'defalt', isFooter, children } = props

  return (
    <div className="layout">
      <Header />
      <SideBar />
      <SearchTag searchtags={searchtags} isAuth={true} />
      <Meta title={title} />
      <Main title={title} search={search} type={type}>
        {children}
        {isFooter && <Footer />}
      </Main>
    </div>
  )
}
