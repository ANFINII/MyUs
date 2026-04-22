import cx from 'utils/functions/cx'
import IconError from 'components/parts/Icon/Error'
import IconInfo from 'components/parts/Icon/Info'
import IconWarning from 'components/parts/Icon/Warning'
import style from './Alert.module.scss'

const iconMap = {
  info: IconInfo,
  warning: IconWarning,
  error: IconError,
}

type AlertType = 'info' | 'warning' | 'error'

interface Props {
  type?: AlertType
  className?: string
  children: React.ReactNode
}

export default function Alert(props: Props): React.JSX.Element {
  const { type = 'info', className, children } = props

  const Icon = iconMap[type]

  return (
    <div className={cx(style.alert, style[type], className)}>
      <span className={style.icon}>
        <Icon size="16" />
      </span>
      <div className={style.content}>{children}</div>
    </div>
  )
}
