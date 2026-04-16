import cx from 'utils/functions/cx'
import IconChevront from 'components/parts/Icon/Chevront'
import style from './ArrowButton.module.scss'

interface Props {
  type: 'left' | 'right'
  disabled: boolean
  onClick: () => void
}

export default function ArrowButton(props: Props): React.JSX.Element {
  const { type, disabled, onClick } = props

  return (
    <button type="button" className={cx(style.button, disabled && style.disabled)} disabled={disabled} onClick={onClick}>
      <IconChevront width="12" height="12" type={type} />
    </button>
  )
}
