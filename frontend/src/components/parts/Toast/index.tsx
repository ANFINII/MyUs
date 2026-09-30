import cx from 'utils/functions/cx'
import IconCross from 'components/parts/Icon/Cross'
import style from './Toast.module.scss'

export interface Props {
  content?: string
  isError?: boolean
  isToast?: boolean
  setIsToast?: React.Dispatch<React.SetStateAction<boolean>>
}

export default function Toast(props: Props): React.JSX.Element {
  const { content, isError, isToast, setIsToast } = props

  const handleClose = () => setIsToast?.(false)

  return (
    <div className={cx(style.cover, isToast && style.active)}>
      <div className={cx(style.toast, isError && style.error)}>
        <span className={style.content}>{content}</span>
        <span className={style.cross} onClick={handleClose}>
          <IconCross size="22" />
        </span>
      </div>
    </div>
  )
}
