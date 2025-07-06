import IconCaret from 'components/parts/Icon/Caret'
import style from './ThreadView.module.scss'

interface Props {
  isView: boolean
  count: number
  onClick: () => void
}

export default function ThreadView(props: Props): JSX.Element {
  const { isView, count, onClick } = props

  return (
    <label className={style.thread} onClick={onClick}>
      <div className={style.icon}>
        <IconCaret size="16" type={isView ? 'down' : 'right'} />
      </div>
      <span className={style.reply_count}>スレッド {count} 件</span>
    </label>
  )
}
