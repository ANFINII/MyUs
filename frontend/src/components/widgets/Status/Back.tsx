import { useTranslation } from 'react-i18next'
import { useRouter } from 'components/hooks/useRouter'
import Button from 'components/parts/Button'
import style from './Status.module.scss'

interface Props {
  content: string
}

export default function BackError(props: Props): React.JSX.Element {
  const { content } = props

  const router = useRouter()
  const { t } = useTranslation()

  const handleBack = () => {
    if (router.canBack()) {
      router.back()
    } else {
      router.replace('/')
    }
    setTimeout(() => router.reload(), 100)
  }

  return (
    <>
      <h2 className={style.error}>{content}</h2>
      <Button name={t('status.back')} className={style.button} onClick={handleBack} />
    </>
  )
}
