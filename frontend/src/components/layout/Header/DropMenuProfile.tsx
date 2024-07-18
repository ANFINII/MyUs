import Link from 'next/link'
import { useRouter } from 'next/router'
import clsx from 'clsx'
import { postLogout } from 'api/auth'
import { isActive } from 'utils/functions/common'
import { useUser } from 'components/hooks/useUser'
import IconArrow from 'components/parts/Icon/Arrow'
import IconCredit from 'components/parts/Icon/Credit'
import IconGrid from 'components/parts/Icon/Grid'
import IconPencil from 'components/parts/Icon/Pencil'
import IconPerson from 'components/parts/Icon/Person'

interface Props {
  open: boolean
  onClose: () => void
}

export default function DropMenuProfile(props: Props) {
  const { open, onClose } = props

  const router = useRouter()
  const { user, resetUser } = useUser()

  const handleClick = (url: string) => {
    router.push(url)
    onClose()
  }

  const handleIn = () => router.push('/login')

  const handleLogout = async () => {
    router.push('/login')
    await postLogout()
    resetUser()
  }

  return (
    <nav className={clsx('drop_menu drop_menu_profile', isActive(open))}>
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
          <Link href={user.isStaff || user.isActive ? '/' : '/login'} className="icon_link"></Link>
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

        {user.isActive && !user.isStaff && (
          <li className="drop_menu_list" onClick={() => handleClick('/setting/withdrawal')}>
            <IconPerson size="1.5em" type="cross" className="color_drop_menu_bi" />
            <span>退会処理</span>
          </li>
        )}

        <li className="drop_menu_list" onClick={handleIn}>
          <IconArrow size="1.5em" type="in" className="color_drop_menu_bi" />
          <span>ログイン</span>
        </li>

        <li className="drop_menu_list" onClick={handleLogout}>
          <IconArrow size="1.5em" type="out" className="color_drop_menu_bi" />
          <span>ログアウト</span>
        </li>
      </ul>
    </nav>
  )
}
