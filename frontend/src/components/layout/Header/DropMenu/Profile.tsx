import { useRouter } from 'next/router'
import clsx from 'clsx'
import { postLogout } from 'api/internal/auth'
import { isActive } from 'utils/functions/common'
import { useUser } from 'components/hooks/useUser'
import IconArrow from 'components/parts/Icon/Arrow'
import IconCredit from 'components/parts/Icon/Credit'
import IconGrid from 'components/parts/Icon/Grid'
import IconPencil from 'components/parts/Icon/Pencil'
import IconPerson from 'components/parts/Icon/Person'
import DropMenuItem from 'components/parts/NavItem/DropMenuItem'

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

  const handleLogin = () => router.push('/account/login')

  const handleLogout = async () => {
    handleLogin()
    await postLogout()
    resetUser()
  }

  const handleManagement = () => {
    if (user.isStaff) {
      router.push('http://127.0.0.1:8000/myus-admin')
    } else if (user.isActive) {
      router.push('http://127.0.0.1:8000/myus-manage')
    } else {
      router.push('/')
    }
    onClose()
  }

  return (
    <nav className={clsx('drop_menu drop_menu_profile', isActive(open))}>
      <ul>
        <DropMenuItem label="アカウント" icon={<IconPerson size="1.5em" type="circle" />} onClick={() => handleClick('/setting/profile')} />
        <DropMenuItem label="マイページ" icon={<IconPerson size="1.5em" type="square" />} onClick={() => handleClick('/setting/mypage')} />
        <DropMenuItem label="投稿管理" icon={<IconGrid size="1.5em" />} onClick={handleManagement} />
        <DropMenuItem label="ToDo" icon={<IconPencil size="1.5em" />} onClick={() => handleClick('/media/todo')} />
        <DropMenuItem label="料金プラン" icon={<IconCredit size="1.5em" />} onClick={() => handleClick('/setting/payment')} />
        <DropMenuItem label="退会処理" icon={<IconPerson size="1.5em" type="cross" />} onClick={() => handleClick('/setting/withdrawal')} />
        <DropMenuItem label="ログイン" icon={<IconArrow size="1.5em" type="in" />} onClick={handleLogin} />
        <DropMenuItem label="ログアウト" icon={<IconArrow size="1.5em" type="out" />} onClick={handleLogout} />
      </ul>
    </nav>
  )
}
