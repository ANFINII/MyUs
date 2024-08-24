import { useState } from 'react'
import Link from 'next/link'
import clsx from 'clsx'
import { isActive } from 'utils/functions/common'
import { useUser } from 'components/hooks/useUser'
import DropMenuCloud from 'components/layout/Header/DropMenuCloud'
import DropMenuNotice from 'components/layout/Header/DropMenuNotice'
import DropMenuProfile from 'components/layout/Header/DropMenuProfile'
import SideMenu from 'components/layout/Header/SideMenu'
import Avatar from 'components/parts/Avatar'
import IconBell from 'components/parts/Icon/Bell'
import IconCloud from 'components/parts/Icon/Cloud'
import IconExclamation from 'components/parts/Icon/Exclamation'
import IconLightning from 'components/parts/Icon/Lightning'
import IconList from 'components/parts/Icon/List'
import Search from 'components/parts/Input/Search'

interface Props {
  loading?: boolean
}

export default function Header(props: Props) {
  const { loading } = props

  const { user } = useUser()
  const [search, setSearch] = useState<string>('')
  const [isSideMenu, setIsSideMenu] = useState<boolean>(false)
  const [isCloud, setIsCloud] = useState<boolean>(false)
  const [isNotice, setIsNotice] = useState<boolean>(false)
  const [isProfile, setIsProfile] = useState<boolean>(false)

  const handleSearch = (value: string) => setSearch(value)
  const handleSideMenu = () => setIsSideMenu(!isSideMenu)
  const handleCloud = () => setIsCloud(!isCloud)
  const handleNotice = () => setIsNotice(!isNotice)
  const handleProfile = () => setIsProfile(!isProfile)

  const handleCoverClose = () => {
    setIsCloud(false)
    setIsNotice(false)
    setIsProfile(false)
  }

  const notificationCount = 0

  return (
    <header className={clsx('header', loading ? 'loading' : '')}>
      <nav className="header_nav">
        <div className={clsx('side_nemu_cover', isActive(isSideMenu))} onClick={handleSideMenu}></div>
        <div className={clsx('drop_back_cover', isActive(isCloud || isNotice || isProfile))} onClick={handleCoverClose}></div>

        <div className="header_nav_1 header_color" onClick={handleSideMenu}>
          <IconList width="2em" height="1.7em" />
          <SideMenu open={isSideMenu} onClose={handleSideMenu} />
        </div>

        <div className="header_nav_2 header_color_MyUs">
          <Link href="/" className="icon_link"></Link>
          <h1>MyUs</h1>
        </div>

        <div className="header_nav_3 search_box">
          <Search value={search} onChange={handleSearch} />
        </div>

        <div className="header_nav_4 header_color">
          <Link href="/recommend" className="icon_link"></Link>
          <IconLightning size="1.5em" type="fill" />
        </div>

        <div className={clsx('header_nav_5 header_color', isActive(isCloud))} onClick={handleCloud}>
          <IconCloud size="1.5em" />
          <DropMenuCloud open={isCloud} onClose={handleCloud} />
        </div>

        <div className={clsx('header_nav_6 header_color', isActive(isNotice))} onClick={handleNotice}>
          <IconBell size="1.5em" className={isActive(notificationCount > 0)} />
          <IconExclamation size="1.2em" className={isActive(notificationCount > 0)} />
          <DropMenuNotice open={isNotice} onClose={handleNotice} />
        </div>

        <div className={clsx('header_nav_7 header_color', isActive(isProfile))} onClick={handleProfile}>
          <Avatar size="1.8em" imgSize="32" src={user.avatar} nickname={user.nickname} className={clsx('account', isActive(isProfile))} />
          <DropMenuProfile open={isProfile} onClose={handleProfile} />
        </div>
      </nav>
    </header>
  )
}
