import ToggleOn from "components/parts/Icon/ToggleOn"
import ToggleOff from "components/parts/Icon/ToggleOff"
import style from 'components/parts/Input/Toggle/Toggle.module.css'

interface Props {
  isActive: boolean
  onClick: () => void
}

export default function Toggle(props: Props) {
  const {isActive, onClick} = props

  return (
    <div className={style.radio + (isActive ? ' ' + style.active : '')} onClick={onClick}>
      {isActive ? <ToggleOn /> : <ToggleOff />}
    </div>
  )
}
