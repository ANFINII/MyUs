import { useEffect } from 'react'
import clsx from 'clsx'
import style from './Toast.module.scss'
import IconCross from '../Icon/Cross'

export interface Props {
  toastContent?: string
  isError?: boolean
  isToast?: boolean
  setIsToast?: React.Dispatch<React.SetStateAction<boolean>>
}

export default function Toast(props: Props): JSX.Element {
  const { toastContent, isError, isToast, setIsToast } = props

  useEffect(() => {
    if (isToast) {
      const timer = setTimeout(() => setIsToast && setIsToast(false), 5000)
      return () => clearTimeout(timer)
    }
  }, [isToast, setIsToast])

  const handleClose = () => setIsToast && setIsToast(false)

  return (
    <div className={clsx(style.cover, isToast ? style.active : '')}>
      <div className={clsx(style.toast, isError ? style.error : '')}>
        <span className={style.content}>{toastContent}</span>
        <span className={style.cross} onClick={handleClose}>
          <IconCross size="22" />
        </span>
      </div>
    </div>
  )
}
