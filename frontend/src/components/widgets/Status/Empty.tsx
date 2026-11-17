import cx from 'utils/functions/cx'
import style from './Status.module.scss'

interface Props {
  content: string
  className?: string
}

export default function Empty(props: Props): React.JSX.Element {
  const { content, className } = props

  return <p className={cx(style.empty, className)}>{content}</p>
}
