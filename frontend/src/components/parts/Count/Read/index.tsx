import IconCaret from 'components/parts/Icon/Caret'
import style from './Read.module.scss'

interface Props {
  read?: number
}

export default function CountRead(props: Props): React.JSX.Element {
  const { read } = props

  return (
    <div className={style.count}>
      <div className={style.icon}>
        <IconCaret size="16" className="mr_8" />
      </div>
      <span>{read}</span>
    </div>
  )
}
