import { useState } from 'react'
import Link from 'next/link'
import DropMenuCloud from 'components/layout/Header/DropMenuCloud'
import DropMenuNotice from 'components/layout/Header/DropMenuNotice'
import DropMenuProfile from 'components/layout/Header/DropMenuProfile'
import SideMenu from 'components/layout/Header/SideMenu'

export default function Header() {
  const [search, setSearch] = useState<string>('')
  const [isOpenCloud, setIsOpenCloud] = useState<boolean>(false)
  const [isOpenNotice, setIsOpenNotice] = useState<boolean>(false)
  const [isOpenProfile, setIsOpenProfile] = useState<boolean>(false)

  const handleCloud = () => {
    setIsOpenCloud(!isOpenCloud)
    setIsOpenNotice(false)
    setIsOpenProfile(false)
  }
  const handleNotice = () => setIsOpenNotice(!isOpenNotice)
  const handleProfile = () => setIsOpenProfile(!isOpenProfile)

  return (
    <header className="header">
      <nav className="header_nav">
        <div className="header_nav_1">
          <SideMenu />
        </div>

        <div className="header_nav_2 header_color_MyUs">
          <Link href="/" className="icon_link"></Link>
          <h1>MyUs</h1>
        </div>

        <div className="header_nav_3">
          <div className="search_container">
            <div className="searchbar">
              <form method="GET" action="">
                <input type="search" name="search" value={search} placeholder="検索..." className="search_input" />
                <button type="submit" className="search_icon">
                  <i className="fas fa-search"></i>
                </button>
              </form>
            </div>
          </div>
        </div>

        <div className="header_nav_4 header_color">
          <Link href="/recommend" className="icon_link"></Link>
          <svg xmlns="http://www.w3.org/2000/svg" width="1.5em" height="1.5em" fill="currentColor" className="bi bi-lightning-charge-fill" viewBox="0 0 16 16">
            <path d="M11.251.068a.5.5 0 0 1 .227.58L9.677 6.5H13a.5.5 0 0 1 .364.843l-8 8.5a.5.5 0 0 1-.842-.49L6.323 9.5H3a.5.5 0 0 1-.364-.843l8-8.5a.5.5 0 0 1 .615-.09z" />
          </svg>
        </div>

        <div className="header_nav_5 header_color" onClick={handleCloud}>
          <DropMenuCloud isOpen={isOpenCloud} setIsOpen={setIsOpenCloud} />
        </div>

        <div className="header_nav_6 header_color" onClick={handleNotice}>
          <DropMenuNotice isOpen={isOpenNotice} setIsOpen={setIsOpenNotice} />
        </div>

        <div className="header_nav_7" onClick={handleProfile}>
          <DropMenuProfile isActive isStaff={false} isOpen={isOpenProfile} setIsOpen={setIsOpenProfile} />
        </div>
      </nav>
    </header>
  )
}
