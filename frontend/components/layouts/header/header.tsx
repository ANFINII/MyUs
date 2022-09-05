import Link from 'next/link'
import SideMenu from 'components/layouts/header/side_menu'
import DropMenuCloud from 'components/layouts/header/drop_menu_cloud'
import DropMenuNotice from 'components/layouts/header/drop_menu_notice'
import DropMenuProfile from 'components/layouts/header/drop_menu_profile'

export default function Header() {
  return (
    <header className="header">
      <nav className="header_nav">
        <div className="header_nav_1">
          <SideMenu/>
        </div>

        <div className="header_nav_2 color_header_MyUs">
          <div><h1>MyUs</h1></div>
          <Link href="/">
            <a className="icon_link" role="button" aria-disabled="true"></a>
          </Link>
        </div>

        <div className="header_nav_3 color_header">
          <div className="search_container">
            <div className="d-flex justify-content-center">
              <div className="searchbar">
                <form method="GET" action="">
                  <input type="search" name="search" value="{{ request.GET.search }}" placeholder="検索..." className="search_input"/>
                  <button type="submit" className="search_icon"><i className="fas fa-search"></i></button>
                </form>
              </div>
            </div>
          </div>
        </div>

        <div className="header_nav_4 color_header">
          <svg xmlns="http://www.w3.org/2000/svg" width="1.5em" height="1.5em" fill="currentColor" className="bi bi-lightning-charge-fill" viewBox="0 0 16 16">
            <path d="M11.251.068a.5.5 0 0 1 .227.58L9.677 6.5H13a.5.5 0 0 1 .364.843l-8 8.5a.5.5 0 0 1-.842-.49L6.323 9.5H3a.5.5 0 0 1-.364-.843l8-8.5a.5.5 0 0 1 .615-.09z"/>
          </svg>
          <Link href="/recommend">
            <a className="icon_link" role="button" aria-disabled="true"></a>
          </Link>
        </div>

        <div className="header_nav_5 color_header">
          <DropMenuCloud/>
        </div>

        <div className="header_nav_6 color_header">
          <DropMenuNotice/>
        </div>

        <div className="header_nav_7 color_header">
          <DropMenuProfile/>
        </div>
      </nav>
    </header>
  )
}
