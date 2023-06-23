import Header from 'components/layouts/Header'
import SideBar from 'components/layouts/SideBar'
import SearchTag from 'components/layouts/SearchTag'

interface Props {children: React.ReactNode}

interface searchtag {
  name: string
}

export default function Layout(props: Props) {
  const {children} = props

  const searchtagData: searchtag[] = [{name: '初音ミク'}, {name: 'VOCALOID'}, {name: '宇宙'}]

  return (
    <div className="layout">
      <Header />
      <SideBar />
      <SearchTag searchtag={searchtagData} isAuthenticated={true} />
      {children}
    </div>
  )
}
