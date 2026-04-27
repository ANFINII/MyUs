import { useRouter } from 'next/router'
import { postLogout } from 'api/internal/auth'
import cx from 'utils/functions/cx'
import { useUser } from 'components/hooks/useUser'
import IconArrow from 'components/parts/Icon/Arrow'
import IconCredit from 'components/parts/Icon/Credit'
import IconPerson from 'components/parts/Icon/Person'
import NavItem from 'components/parts/NavItem'
import style from './DropMenu.module.scss'

interface Props {
  open: boolean
  onClose: () => void
}

export default function DropMenuProfile(props: Props): React.JSX.Element {
  const { open, onClose } = props

  const router = useRouter()
  const { resetUser } = useUser()

  const handleRouter = (url: string) => {
    router.push(url)
    onClose()
  }

  const handleLogin = () => handleRouter('/account/login')

  const handleLogout = async () => {
    await handleLogin()
    const ret = await postLogout()
    if (ret.isErr()) return
    resetUser()
  }

  return (
    <nav className={cx(style.drop_menu, open && style.active)}>
      <ul>
        <NavItem label="アカウント" icon={<IconPerson size="1.5em" type="circle" />} className={style.item} onClick={() => handleRouter('/setting/profile')} />
        <NavItem label="マイページ" icon={<IconPerson size="1.5em" type="square" />} className={style.item} onClick={() => handleRouter('/setting/mypage')} />
        <NavItem label="料金プラン" icon={<IconCredit size="1.5em" />} className={style.item} onClick={() => handleRouter('/setting/payment')} />
        <NavItem label="退会処理" icon={<IconPerson size="1.5em" type="cross" />} className={style.item} onClick={() => handleRouter('/setting/withdrawal')} />
        <NavItem label="ログイン" icon={<IconArrow size="1.5em" type="in" />} className={style.item} onClick={handleLogin} />
        <NavItem label="ログアウト" icon={<IconArrow size="1.5em" type="out" />} className={style.item} onClick={handleLogout} />
      </ul>
    </nav>
  )
}
