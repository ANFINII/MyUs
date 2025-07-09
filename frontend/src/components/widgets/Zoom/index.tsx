import clsx from 'clsx'
import IconCaret from 'components/parts/Icon/Caret'
import style from './Zoom.module.scss'

interface Props {
  isView: boolean
  onView: () => void
  size?: 's' | 'm' | 'l'
  content: string
}

export default function Zoom(props: Props): JSX.Element {
  const { isView, onView, size = 'm', content } = props

  return (
    <label className={clsx(style.zoom, isView && style.active, style[size])} onClick={onView}>
      <div className={style.icon}>
        <IconCaret size="16" type={isView ? 'down' : 'right'} />
      </div>
      <p className="us_none">{content}</p>
    </label>
  )
}
