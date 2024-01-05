import IconToggleOff from 'components/parts/Icon/ToggleOff'
import IconToggleOn from 'components/parts/Icon/ToggleOn'
import style from 'components/parts/Input/Toggle/Toggle.module.css'

interface Props {
  isActive: boolean
  onClick: () => void
}

export default function Toggle(props: Props) {
  const { isActive, onClick } = props

  return (
    <div className={style.radio + (isActive && ' ' + style.active)} onClick={onClick}>
      {isActive ? <IconToggleOn size="25" /> : <IconToggleOff size="25" />}
    </div>
  )
}
