import { useTranslation } from 'react-i18next'
import { useNavigate, useRouter } from '@tanstack/react-router'
import Button from 'components/parts/Button'
import style from './Status.module.scss'

interface Props {
  content: string
}

export default function BackError(props: Props): React.JSX.Element {
  const { content } = props

  const router = useRouter()
  const navigate = useNavigate()
  const { t } = useTranslation()

  const handleBack = () => {
    if (window.history.length > 1) {
      router.history.back()
    } else {
      navigate({ to: '/', replace: true })
    }
    setTimeout(() => window.location.reload(), 100)
  }

  return (
    <>
      <h2 className={style.error}>{content}</h2>
      <Button name={t('status.back')} className={style.button} onClick={handleBack} />
    </>
  )
}
