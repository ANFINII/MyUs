import { useRouter } from 'next/router'
import { postLogout } from 'api/auth'
import IconArrow from 'components/parts/Icon/Arrow'
import IconCredit from 'components/parts/Icon/Credit'
import IconGrid from 'components/parts/Icon/Grid'
import IconPencil from 'components/parts/Icon/Pencil'
import IconPerson from 'components/parts/Icon/Person'

interface Props {
  isOpen: boolean
  setIsOpen: React.Dispatch<React.SetStateAction<boolean>>
  isActive?: boolean
  isStaff?: boolean
}

export default function DropMenuProfile(props: Props) {
  const { isOpen, setIsOpen, isActive, isStaff } = props

  const router = useRouter()

  const handleClick = (url: string) => {
    router.push(url)
    setIsOpen(false)
  }

  const handleLogout = async () => {
    await postLogout()
    localStorage.removeItem('user')
    router.push('/login')
  }

  return (
    <nav className={'drop_menu drop_menu_profile' + (isOpen ? ' ' + 'active' : '')}>
      <ul>
        <li className="drop_menu_list" onClick={() => handleClick('/setting/profile')}>
          <IconPerson size="1.5em" type="circle" className="color_drop_menu_bi" />
          <span>アカウント</span>
        </li>

        <li className="drop_menu_list" onClick={() => handleClick('/setting/mypage')}>
          <IconPerson size="1.5em" type="square" className="color_drop_menu_bi" />
          <span>マイページ</span>
        </li>

        <li className="drop_menu_list" onClick={() => handleClick('/media/todo')}>
          {/* <Link href={isStaff || isActive ? '/' : '/login'} className="icon_link"></Link> */}
          <IconGrid size="1.5em" className="color_drop_menu_bi" />
          <span>投稿管理</span>
        </li>

        <li className="drop_menu_list" onClick={() => handleClick('/media/todo')}>
          <IconPencil size="1.5em" className="color_drop_menu_bi" />
          <span>ToDo</span>
        </li>

        <li className="drop_menu_list" onClick={() => handleClick('/setting/payment')}>
          <IconCredit size="1.5em" className="color_drop_menu_bi" />
          <span>料金プラン</span>
        </li>

        {!isStaff && (
          <li className="drop_menu_list" onClick={() => handleClick('/setting/withdrawal')}>
            <IconPerson size="1.5em" type="cross" className="color_drop_menu_bi" />
            <span>退会処理</span>
          </li>
        )}

        <li className="drop_menu_list" onClick={handleLogout}>
          <IconArrow size="1.5em" type="box" className="color_drop_menu_bi" />
          <span>ログアウト</span>
        </li>
      </ul>
    </nav>
  )
}
