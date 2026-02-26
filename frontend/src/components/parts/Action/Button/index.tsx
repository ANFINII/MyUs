import { useRef } from 'react'
import clsx from 'clsx'
import IconDots from 'components/parts/Icon/Dots'
import style from './ActionButton.module.scss'
import ActionList, { ActionItem } from '../List'

interface Props {
  open: boolean
  onMenu: () => void
  isRound?: boolean
  disabled?: boolean
  actionItems: ActionItem[]
}

export default function ActionButton(props: Props): React.JSX.Element {
  const { open, onMenu, isRound = false, disabled = false, actionItems } = props

  const actionRef = useRef<HTMLButtonElement>(null)

  return (
    <div className={clsx(style.action, isRound && style.isRound)}>
      <button ref={actionRef} className={style.action_button} disabled={disabled} onClick={onMenu}>
        <IconDots size="18" />
      </button>
      <div className={style.action_list}>
        <ActionList triggerRef={actionRef} open={open} onClose={onMenu} items={actionItems} />
      </div>
    </div>
  )
}
