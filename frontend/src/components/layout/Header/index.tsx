import { ChangeEvent, useState } from 'react'
import { useRouter } from 'next/router'
import cx from 'utils/functions/cx'
import { useUser } from 'components/hooks/useUser'
import DropMenuCloud from 'components/layout/Header/DropMenu/Cloud'
import DropMenuNotice from 'components/layout/Header/DropMenu/Notice'
import DropMenuProfile from 'components/layout/Header/DropMenu/Profile'
import SideMenu from 'components/layout/Header/SideMenu'
import Avatar from 'components/parts/Avatar'
import IconBell from 'components/parts/Icon/Bell'
import IconCloud from 'components/parts/Icon/Cloud'
import IconExclamation from 'components/parts/Icon/Exclamation'
import IconLightning from 'components/parts/Icon/Lightning'
import IconList from 'components/parts/Icon/List'
import Search from 'components/parts/Input/Search'
import style from './Header.module.scss'

interface Props {
  loading?: boolean
}

export default function Header(props: Props): React.JSX.Element {
  const { loading } = props

  const router = useRouter()
  const { user } = useUser()
  const [isSideMenu, setIsSideMenu] = useState<boolean>(false)
  const [isCloud, setIsCloud] = useState<boolean>(false)
  const [isNotice, setIsNotice] = useState<boolean>(false)
  const [isProfile, setIsProfile] = useState<boolean>(false)
  const [search, setSearch] = useState<string>('')

  const handleRouter = (url: string) => router.push(url)
  const handleSideMenu = () => setIsSideMenu(!isSideMenu)
  const handleCloud = () => setIsCloud(!isCloud)
  const handleNotice = () => setIsNotice(!isNotice)
  const handleProfile = () => setIsProfile(!isProfile)
  const handleSearch = (e: ChangeEvent<HTMLInputElement>) => setSearch(e.target.value)

  const handleCoverClose = () => {
    setIsCloud(false)
    setIsNotice(false)
    setIsProfile(false)
  }

  const notificationCount = 0

  return (
    <header className={cx(style.header, loading && style.loading)}>
      <nav className={style.nav}>
        <div className={cx(style.side_menu_cover, isSideMenu && style.active)} onClick={handleSideMenu}></div>
        <div className={cx(style.drop_back_cover, (isCloud || isNotice || isProfile) && style.active)} onClick={handleCoverClose}></div>

        <div className={cx(style.nav_1, style.color)} onClick={handleSideMenu}>
          <IconList width="2em" height="1.7em" />
          <SideMenu open={isSideMenu} onClose={handleSideMenu} />
        </div>

        <div className={cx(style.nav_2, style.color_MyUs)} onClick={() => handleRouter('/')}>
          <h1>MyUs</h1>
        </div>

        <div className={cx(style.nav_3, style.search_box)}>
          <Search value={search} onChange={handleSearch} />
        </div>

        <div className={cx(style.nav_4, style.color)} onClick={() => handleRouter('/recommend')}>
          <IconLightning size="1.5em" type="fill" />
        </div>

        <div className={cx(style.nav_5, style.color, isCloud && style.active)} onClick={handleCloud}>
          <IconCloud size="1.5em" />
          <DropMenuCloud open={isCloud} onClose={handleCloud} />
        </div>

        <div className={cx(style.nav_6, style.color, isNotice && style.active)} onClick={handleNotice}>
          <IconBell size="1.5em" className={cx(style.bell, notificationCount > 0 && style.active)} />
          <IconExclamation size="1.2em" className={cx(style.exclamation, notificationCount > 0 && style.active)} />
          <DropMenuNotice open={isNotice} onClose={handleNotice} />
        </div>

        <div className={cx(style.nav_7, style.color, isProfile && style.active)} onClick={handleProfile}>
          <Avatar src={user.avatar} title={user.nickname} size="32" className={cx(style.account, isProfile && style.active)} />
          <DropMenuProfile open={isProfile} onClose={handleProfile} />
        </div>
      </nav>
    </header>
  )
}
