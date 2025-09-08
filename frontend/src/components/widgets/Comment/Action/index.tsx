import { RefObject } from 'react'
import ActionList, { ActionItem } from 'components/parts/ActionList'
import IconDots from 'components/parts/Icon/Dots'
import style from './Action.module.scss'

export interface Props {
  open: boolean
  onMenu: () => void
  actionRef: RefObject<HTMLButtonElement | null>
  disabled: boolean
  actionItems: ActionItem[]
}

export default function CommentAction(props: Props): React.JSX.Element {
  const { open, onMenu, actionRef, disabled, actionItems } = props

  return (
    <div className={style.action_wrap}>
      <button ref={actionRef} className={style.action_button} disabled={disabled} onClick={onMenu}>
        <IconDots size="18" />
      </button>
      <div className={style.action_list}>
        <ActionList triggerRef={actionRef} open={open} onClose={onMenu} items={actionItems} />
      </div>
    </div>
  )
}
