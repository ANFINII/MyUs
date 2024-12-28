import { useEffect } from 'react'
import clsx from 'clsx'
import style from './Toast.module.scss'
import IconCross from '../Icon/Cross'

export interface Props {
  content?: string
  isError?: boolean
  isToast?: boolean
  setIsToast?: React.Dispatch<React.SetStateAction<boolean>>
}

export default function Toast(props: Props) {
  const { content, isError, isToast, setIsToast } = props

  useEffect(() => {
    if (isToast) {
      setTimeout(() => setIsToast && setIsToast(false), 5000)
    }
  }, [isToast, setIsToast])

  const handleClose = () => setIsToast && setIsToast(false)

  return (
    <div className={clsx(style.cover, isToast ? style.active : '')}>
      <div className={clsx(style.toast, isError ? style.error : '')}>
        <span className={style.content}>{content}</span>
        <span className={style.cross} onClick={handleClose}>
          <IconCross size="22" />
        </span>
      </div>
    </div>
  )
}
