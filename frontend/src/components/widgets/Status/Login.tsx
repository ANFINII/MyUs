import { useTranslation } from 'react-i18next'
import { useNavigate } from '@tanstack/react-router'
import Button from 'components/parts/Button'
import style from './Status.module.scss'

interface Props {
  content: string
}

export default function BackLogin(props: Props): React.JSX.Element {
  const { content } = props

  const navigate = useNavigate()
  const { t } = useTranslation()

  const handleLogin = () => {
    navigate({ to: '/account/login' })
  }

  return (
    <>
      <h2 className={style.error}>{content}</h2>
      <Button name={t('status.login')} className={style.button} onClick={handleLogin} />
    </>
  )
}
