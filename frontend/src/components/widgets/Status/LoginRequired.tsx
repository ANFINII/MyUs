import { useTranslation } from 'react-i18next'
import cx from 'utils/functions/cx'
import { useRouter } from 'components/hooks/useRouter'
import Button from 'components/parts/Button'
import style from './Status.module.scss'

interface Props {
  className?: string
}

export default function LoginRequired(props: Props): React.JSX.Element {
  const { className } = props

  const router = useRouter()
  const { t } = useTranslation()

  const handleLogin = () => router.push('/account/login')

  return (
    <div className={cx(style.login_required, className)}>
      <p>{t('status.loginRequired')}</p>
      <Button name={t('status.login')} color="blue" onClick={handleLogin} />
    </div>
  )
}
