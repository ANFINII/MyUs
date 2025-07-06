import IconCaret from 'components/parts/Icon/Caret'
import style from './ReplyView.module.scss'

interface Props {
  isView: boolean
  onClick: () => void
}

export default function ReplyView(props: Props): JSX.Element {
  const { isView, onClick } = props

  return (
    <label className={style.reply} onClick={onClick}>
      <div className={style.icon}>
        <IconCaret size="16" type={isView ? 'down' : 'right'} />
      </div>
      <p className="us_none">返信</p>
    </label>
  )
}
