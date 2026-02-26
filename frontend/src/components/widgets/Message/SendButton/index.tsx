import IconCaret from 'components/parts/Icon/Caret'
import style from './SendButton.module.scss'

interface Props {
  disabled?: boolean
}

export default function SendButton(props: Props): React.JSX.Element {
  const { disabled = false } = props

  return (
    <button type="submit" className={style.send_button} disabled={disabled}>
      <IconCaret size="16" type="right" />
    </button>
  )
}
