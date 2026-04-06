import { useRef, RefObject } from 'react'
import cx from 'utils/functions/cx'
import { useClickOutside } from 'components/hooks/useClickOutside'
import style from './ActionList.module.scss'

export interface ActionItem {
  icon: React.ReactNode
  label: string
  onClick: () => void
  danger?: boolean
}

interface Props {
  open: boolean
  onClose?: () => void
  size?: 's' | 'm' | 'l'
  triggerRef: RefObject<HTMLElement | null>
  items: ActionItem[]
}

export default function ActionList(props: Props): React.JSX.Element {
  const { open, onClose, size = 'm', triggerRef, items } = props

  const actionRef = useRef<HTMLDivElement>(null)
  useClickOutside({ actionRef, triggerRef, isActive: open, onClick: () => onClose?.() })

  const handleItemClick = (item: ActionItem) => () => {
    item.onClick()
    onClose?.()
  }

  return (
    <>
      {open && (
        <div ref={actionRef} className={cx(style.action_list, style[size])}>
          {items.map((item, index) => (
            <button key={index} className={cx(style.item, item.danger && style.danger)} onClick={handleItemClick(item)}>
              <span className={style.icon}>{item.icon}</span>
              <span>{item.label}</span>
            </button>
          ))}
        </div>
      )}
    </>
  )
}
