import cx from 'utils/functions/cx'
import IconToggle from 'components/parts/Icon/Toggle'
import style from './ToggleCard.module.scss'

interface Props {
  label: string
  isActive: boolean
  disable?: boolean
  onClick?: () => void
}

export default function ToggleCard(props: Props): React.JSX.Element {
  const { label, isActive, disable = false, onClick } = props

  return (
    <div className={cx(style.card, isActive && style.active, disable && style.disable)} onClick={onClick}>
      <span className={style.label}>{label}</span>
      <div className={style.toggle}>
        {isActive ? <IconToggle size="25" type="on" /> : <IconToggle size="25" type="off" />}
      </div>
    </div>
  )
}
