import clsx from 'clsx'
import IconToggle from 'components/parts/Icon/Toggle'
import style from './Toggle.module.scss'

interface Props {
  isActive: boolean
  disable?: boolean
  onClick?: () => void
}

export default function Toggle(props: Props): JSX.Element {
  const { isActive, disable = false, onClick } = props

  return (
    <div className={clsx(style.toggle, isActive ? style.active : '', disable ? style.disable : '')} onClick={onClick}>
      {isActive ? <IconToggle size="25" type="on" /> : <IconToggle size="25" type="off" />}
    </div>
  )
}
