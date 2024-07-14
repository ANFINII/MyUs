import { useState } from 'react'
import Link from 'next/link'
import clsx from 'clsx'
import { useUser } from 'components/hooks/useUser'
import DropMenuCloud from 'components/layout/Header/DropMenuCloud'
import DropMenuNotice from 'components/layout/Header/DropMenuNotice'
import DropMenuProfile from 'components/layout/Header/DropMenuProfile'
import SideMenu from 'components/layout/Header/SideMenu'
import ExImage from 'components/parts/ExImage'
import IconBell from 'components/parts/Icon/Bell'
import IconCloud from 'components/parts/Icon/Cloud'
import IconExclamation from 'components/parts/Icon/Exclamation'
import IconLightning from 'components/parts/Icon/Lightning'
import IconList from 'components/parts/Icon/List'
import IconPerson from 'components/parts/Icon/Person'
import Search from 'components/parts/Input/Search'

interface Props {
  loading?: boolean
  nickname?: string
  notificationCount?: number
}

export default function Header(props: Props) {
  const { loading, nickname, notificationCount = 0 } = props

  const { user } = useUser()
  const [search, setSearch] = useState<string>('')
  const [isOpenSideMenu, setIsOpenSideMenu] = useState<boolean>(false)
  const [isOpenCloud, setIsOpenCloud] = useState<boolean>(false)
  const [isOpenNotice, setIsOpenNotice] = useState<boolean>(false)
  const [isOpenProfile, setIsOpenProfile] = useState<boolean>(false)

  const isActive = (isbool: boolean) => (isbool ? 'active' : '')
  const handleSideMenu = () => setIsOpenSideMenu(!isOpenSideMenu)
  const handleCloud = () => setIsOpenCloud(!isOpenCloud)
  const handleNotice = () => setIsOpenNotice(!isOpenNotice)
  const handleProfile = () => setIsOpenProfile(!isOpenProfile)
  const handleSearch = (value: string) => setSearch(value)
  const handleSideMenuClose = (e: React.MouseEvent<HTMLDivElement, MouseEvent>) => e.target === e.currentTarget && setIsOpenSideMenu(false)

  const handleCoverClose = (e: React.MouseEvent<HTMLDivElement, MouseEvent>) => {
    if (e.target === e.currentTarget) {
      setIsOpenCloud(false)
      setIsOpenNotice(false)
      setIsOpenProfile(false)
    }
  }

  return (
    <header className={clsx('header', loading ? 'loading' : '')}>
      <nav className="header_nav">
        <div className={clsx('side_nemu_cover', isActive(isOpenSideMenu))} onClick={handleSideMenuClose}></div>
        <div className={clsx('drop_back_cover', isActive(isOpenCloud || isOpenNotice || isOpenProfile))} onClick={handleCoverClose}></div>

        <button className="header_nav_1 header_color" onClick={handleSideMenu}>
          <IconList width="2em" height="1.7em" />
          <SideMenu isOpen={isOpenSideMenu} setIsOpen={setIsOpenSideMenu} />
        </button>

        <div className="header_nav_2 header_color_MyUs">
          <Link href="/" className="icon_link"></Link>
          <h1>MyUs</h1>
        </div>

        <div className="header_nav_3 search_container">
          <Search value={search} onChange={handleSearch} />
        </div>

        <button className="header_nav_4 header_color">
          <Link href="/recommend" className="icon_link"></Link>
          <IconLightning size="1.5em" type="fill" />
        </button>

        <button className={clsx('header_nav_5 header_color', isActive(isOpenCloud))} onClick={handleCloud}>
          <IconCloud size="1.5em" />
          <DropMenuCloud isOpen={isOpenCloud} setIsOpen={setIsOpenCloud} />
        </button>

        <button className={clsx('header_nav_6 header_color', isActive(isOpenNotice))} onClick={handleNotice}>
          <IconBell size="1.5em" className={isActive(notificationCount > 0)} />
          <IconExclamation size="1.2em" className={isActive(notificationCount > 0)} />
          <DropMenuNotice isOpen={isOpenNotice} setIsOpen={setIsOpenNotice} />
        </button>

        <button className={clsx('header_nav_7 header_color', isActive(isOpenProfile))} onClick={handleProfile}>
          {user.avatar !== '' ? <ExImage src={user.avatar} title={nickname} size="32" className="radius_90" /> : <IconPerson size="1.8em" type="circle" />}
          <DropMenuProfile isOpen={isOpenProfile} setIsOpen={setIsOpenProfile} isActive isStaff={false} />
        </button>
      </nav>
    </header>
  )
}
