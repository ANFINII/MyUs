import router from 'next/router'
import clsx from 'clsx'
import Button from 'components/parts/Button'
import style from './Error.module.scss'

interface Props {
  content: string
}

export default function BackError(props: Props) {
  const { content } = props

  return (
    <>
      <h2 className={clsx(style.error, 'mt_24')}>{content}</h2>
      <Button name="戻る" className="mt_24 w_80" onClick={() => router.back()} />
    </>
  )
}
