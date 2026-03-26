import { formatDate } from 'utils/functions/datetime'
import style from './DateDivider.module.scss'

interface Props {
  created: Date
  prevCreated: Date | null
}

export default function DateDivider(props: Props): React.JSX.Element | null {
  const { created, prevCreated } = props

  const currentDate = new Date(created).toDateString()
  const prevDate = prevCreated ? new Date(prevCreated).toDateString() : ''

  if (currentDate === prevDate) return null

  return (
    <div className={style.date_divider}>
      <span className={style.label}>{formatDate(created)}</span>
    </div>
  )
}
