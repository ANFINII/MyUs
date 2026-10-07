import { useTranslation } from 'react-i18next'
import { postLogout } from 'api/internal/auth'
import cx from 'utils/functions/cx'
import { useAppRouter } from 'components/hooks/useAppRouter'
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

  const router = useAppRouter()
  const { t } = useTranslation()
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
        <NavItem label={t('profileMenu.account')} icon={<IconPerson size="1.5em" type="circle" />} className={style.item} onClick={() => handleRouter('/setting/profile')} />
        <NavItem label={t('profileMenu.mypage')} icon={<IconPerson size="1.5em" type="square" />} className={style.item} onClick={() => handleRouter('/setting/mypage')} />
        <NavItem label={t('profileMenu.payment')} icon={<IconCredit size="1.5em" />} className={style.item} onClick={() => handleRouter('/setting/payment')} />
        <NavItem label={t('profileMenu.withdrawal')} icon={<IconPerson size="1.5em" type="cross" />} className={style.item} onClick={() => handleRouter('/account/withdrawal')} />
        <NavItem label={t('profileMenu.login')} icon={<IconArrow size="1.5em" type="in" />} className={style.item} onClick={handleLogin} />
        <NavItem label={t('profileMenu.logout')} icon={<IconArrow size="1.5em" type="out" />} className={style.item} onClick={handleLogout} />
      </ul>
    </nav>
  )
}
