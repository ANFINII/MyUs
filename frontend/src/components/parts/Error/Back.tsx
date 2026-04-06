import { useRouter } from 'next/router'
import cx from 'utils/functions/cx'
import Button from 'components/parts/Button'
import style from './Error.module.scss'

interface Props {
  content: string
}

export default function BackError(props: Props): React.JSX.Element {
  const { content } = props

  const router = useRouter()

  const handleBack = () => {
    if (window.history.length > 1) {
      router.back()
    } else {
      router.replace('/')
    }
    setTimeout(() => router.reload(), 100)
  }

  return (
    <>
      <h2 className={cx(style.error, 'mt_24')}>{content}</h2>
      <Button name="戻る" className="mt_24 w_80" onClick={handleBack} />
    </>
  )
}
