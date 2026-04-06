import { useRef } from 'react'
import cx from 'utils/functions/cx'
import IconDots from 'components/parts/Icon/Dots'
import style from './ActionButton.module.scss'
import ActionList, { ActionItem } from '../List'

interface Props {
  open: boolean
  onMenu: () => void
  size?: 's' | 'm' | 'l'
  isRound?: boolean
  disabled?: boolean
  actionItems: ActionItem[]
}

export default function ActionButton(props: Props): React.JSX.Element {
  const { open, onMenu, size = 'm', isRound = false, disabled = false, actionItems } = props

  const actionRef = useRef<HTMLButtonElement>(null)

  return (
    <div className={cx(style.action, isRound && style.isRound)}>
      <button ref={actionRef} className={style.action_button} disabled={disabled} onClick={onMenu}>
        <IconDots size="18" />
      </button>
      <div className={style.action_list}>
        <ActionList open={open} onClose={onMenu} size={size} triggerRef={actionRef} items={actionItems} />
      </div>
    </div>
  )
}
