import { RefObject } from 'react'
import ActionList, { ActionItem } from 'components/parts/ActionList'
import IconDots from 'components/parts/Icon/Dots'
import style from './CommentAction.module.scss'

export interface Props {
  open: boolean
  actionRef: RefObject<HTMLButtonElement>
  actionItems: ActionItem[]
  disabled: boolean
  onMenu: () => void
}

export default function CommentAction(props: Props): JSX.Element {
  const { open, actionRef, actionItems, disabled, onMenu } = props

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
