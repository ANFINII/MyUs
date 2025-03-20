import { useRouter } from 'next/router'
import clsx from 'clsx'
import Button from 'components/parts/Button'
import style from './Error.module.scss'

interface Props {
  content: string
}

export default function BackError(props: Props): JSX.Element {
  const { content } = props

  const router = useRouter()

  const handleBack = () => {
    router.back()
    setTimeout(() => router.reload(), 100)
  }

  return (
    <>
      <h2 className={clsx(style.error, 'mt_24')}>{content}</h2>
      <Button name="戻る" className="mt_24 w_80" onClick={handleBack} />
    </>
  )
}
