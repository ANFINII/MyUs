import IconToggle from 'components/parts/Icon/Toggle'
import style from 'components/parts/Input/Toggle/Toggle.module.scss'

interface Props {
  isActive: boolean
  onClick: () => void
}

export default function Toggle(props: Props) {
  const { isActive, onClick } = props

  return (
    <div className={style.radio + (isActive ? ' ' + style.active : '')} onClick={onClick}>
      {isActive ? <IconToggle size="25" type="on" /> : <IconToggle size="25" type="off" />}
    </div>
  )
}
