import { formatDate } from 'utils/functions/datetime'
import Divide from 'components/parts/Divide'

interface Props {
  created: Date
  prevCreated?: Date
}

export default function DateDivider(props: Props): React.JSX.Element {
  const { created, prevCreated } = props

  if (prevCreated === undefined) return <></>

  const currentDate = new Date(created).toDateString()
  const prevDate = new Date(prevCreated).toDateString()

  if (currentDate === prevDate) return <></>

  return <Divide label={formatDate(created)} height="thin" marginV="mv_8" marginH="mh_12" />
}
