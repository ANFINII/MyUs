import IconCaret from 'components/parts/Icon/Caret'
import style from './Zoom.module.scss'

interface Props {
  isView: boolean
  onView: () => void
}

export default function Zoom(props: Props) {
  const { isView, onView } = props

  return (
    <label className={style.zoom} onClick={onView}>
      <div className={style.icon}>
        <IconCaret size="16" type={isView ? 'down' : 'right'} />
      </div>
      <p>{isView ? '縮小表示' : '拡大表示'}</p>
    </label>
  )
}
