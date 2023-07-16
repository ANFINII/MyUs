import Link from 'next/link'
import SideMenu from 'components/layout/Header/SideMenu'
import DropMenuCloud from 'components/layout/Header/DropMenuCloud'
import DropMenuNotice from 'components/layout/Header/DropMenuNotice'
import DropMenuProfile from 'components/layout/Header/DropMenuProfile'

export default function Header() {
  const search = ""
  return (
    <header className="header">
      <nav className="header_nav">
        <div className="header_nav_1">
          <SideMenu />
        </div>

        <div className="header_nav_2 header_color_MyUs">
          <h1>MyUs</h1>
          <Link href="/" className="icon_link"></Link>
        </div>

        <div className="header_nav_3 header_color">
          <div className="search_container">
            <div className="searchbar">
              <form method="GET" action="">
                <input type="search" name="search" value={search} placeholder="検索..." className="search_input" />
                <button type="submit" className="search_icon"><i className="fas fa-search"></i></button>
              </form>
            </div>
          </div>
        </div>

        <div className="header_nav_4 header_color">
          <svg xmlns="http://www.w3.org/2000/svg" width="1.5em" height="1.5em" fill="currentColor" className="bi bi-lightning-charge-fill" viewBox="0 0 16 16">
            <path d="M11.251.068a.5.5 0 0 1 .227.58L9.677 6.5H13a.5.5 0 0 1 .364.843l-8 8.5a.5.5 0 0 1-.842-.49L6.323 9.5H3a.5.5 0 0 1-.364-.843l8-8.5a.5.5 0 0 1 .615-.09z" />
          </svg>
          <Link href="/recommend" className="icon_link"></Link>
        </div>

        <div className="header_nav_5 header_color">
          <DropMenuCloud />
        </div>

        <div className="header_nav_6 header_color">
          <DropMenuNotice />
        </div>

        <div className="header_nav_7">
          <DropMenuProfile nickname="" is_active={true} is_staff={false} />
        </div>
      </nav>
    </header>
  )
}
