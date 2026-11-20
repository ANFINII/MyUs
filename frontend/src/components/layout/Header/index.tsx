import { ChangeEvent, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useQuery } from '@tanstack/react-query'
import { toQuery } from 'lib/query/client'
import { queryKeys } from 'lib/query/keys'
import { getNotification } from 'api/internal/user'
import cx from 'utils/functions/cx'
import { useRouter } from 'components/hooks/useRouter'
import { useUser } from 'components/hooks/useUser'
import DropMenuCloud from 'components/layout/Header/DropMenu/Cloud'
import DropMenuNotice from 'components/layout/Header/DropMenu/Notice'
import DropMenuProfile from 'components/layout/Header/DropMenu/Profile'
import SideMenu from 'components/layout/Header/SideMenu'
import Avatar from 'components/parts/Avatar'
import IconArrow from 'components/parts/Icon/Arrow'
import IconBell from 'components/parts/Icon/Bell'
import IconCloud from 'components/parts/Icon/Cloud'
import IconExclamation from 'components/parts/Icon/Exclamation'
import IconList from 'components/parts/Icon/List'
import Search from 'components/parts/Input/Search'
import Logo from 'components/parts/Logo'
import style from './Header.module.scss'

const NOTIFICATION_STALE_MS = 60 * 1000

interface Props {
  loading?: boolean
}

export default function Header(props: Props): React.JSX.Element {
  const { loading } = props

  const router = useRouter()
  const { t } = useTranslation()
  const { user } = useUser()
  const [isSideMenu, setIsSideMenu] = useState<boolean>(false)
  const [isCloud, setIsCloud] = useState<boolean>(false)
  const [isNotice, setIsNotice] = useState<boolean>(false)
  const [isProfile, setIsProfile] = useState<boolean>(false)
  const [search, setSearch] = useState<string>('')
  const [isSearchBar, setIsSearchBar] = useState<boolean>(false)

  const notificationQuery = useQuery({
    queryKey: queryKeys.notification,
    queryFn: () => toQuery(getNotification()),
    enabled: user.isActive,
    staleTime: NOTIFICATION_STALE_MS,
    refetchOnWindowFocus: true,
  })

  const handleRouter = (url: string) => router.push(url)
  const handleSideMenu = () => setIsSideMenu(!isSideMenu)
  const handleCloud = () => setIsCloud(!isCloud)
  const handleNotice = () => {
    if (!isNotice && user.isActive) notificationQuery.refetch()
    setIsNotice(!isNotice)
  }
  const handleProfile = () => setIsProfile(!isProfile)
  const handleSearch = (e: ChangeEvent<HTMLInputElement>) => setSearch(e.target.value)
  const handleSearchBar = () => setIsSearchBar(!isSearchBar)

  const handleCoverClose = () => {
    setIsCloud(false)
    setIsNotice(false)
    setIsProfile(false)
  }

  const notifications = notificationQuery.data
  const notificationCount = notifications?.count ?? 0

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
          <h1>
            <Logo className={style.logo} />
          </h1>
        </div>

        <div className={cx(style.nav_3, style.search_box)}>
          <Search value={search} onChange={handleSearch} />
          <button type="button" title={t('input.search')} className={style.search_open} onClick={handleSearchBar}></button>
        </div>

        <div className={cx(style.nav_4, style.color, isCloud && style.active)} onClick={handleCloud}>
          <IconCloud size="1.5em" />
          <DropMenuCloud open={isCloud} onClose={handleCloud} />
        </div>

        <div className={cx(style.nav_5, style.color, isNotice && style.active)} onClick={handleNotice}>
          <IconBell size="1.5em" className={cx(style.bell, notificationCount > 0 && style.active)} />
          <IconExclamation size="1.2em" className={cx(style.exclamation, notificationCount > 0 && style.active)} />
          <DropMenuNotice open={isNotice} notifications={notifications} onClose={handleNotice} />
        </div>

        <div className={cx(style.nav_6, style.color, isProfile && style.active)} onClick={handleProfile}>
          <Avatar src={user.avatar} title={user.nickname} size="32" className={cx(style.account, isProfile && style.active)} />
          <DropMenuProfile open={isProfile} onClose={handleProfile} />
        </div>
      </nav>

      {isSearchBar && (
        <div className={style.search_bar}>
          <button type="button" className={cx(style.search_back, style.color)} onClick={handleSearchBar}>
            <IconArrow size="20" type="left" />
          </button>
          <Search value={search} isFull autoFocus onChange={handleSearch} onSearch={handleSearchBar} />
        </div>
      )}
    </header>
  )
}
