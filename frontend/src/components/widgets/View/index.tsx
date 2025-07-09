import clsx from 'clsx'
import IconCaret from 'components/parts/Icon/Caret'
import style from './View.module.scss'

interface Props {
  isView: boolean
  onView: () => void
  size?: 's' | 'm' | 'l'
  color?: 'light' | 'grey'
  content: string
}

export default function View(props: Props): JSX.Element {
  const { isView, onView, size = 'm', content, color = 'light' } = props

  return (
    <label className={clsx(style.view, isView && style.active, style[size], style[color])} onClick={onView}>
      <div className={style.icon}>
        <IconCaret size="16" type={isView ? 'down' : 'right'} />
      </div>
      <p className="us_none">{content}</p>
    </label>
  )
}
