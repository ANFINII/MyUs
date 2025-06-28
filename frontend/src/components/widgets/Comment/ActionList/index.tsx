import { useRef, RefObject } from 'react'
import clsx from 'clsx'
import { useClickOutside } from 'components/hooks/useClickOutside'
import style from './ActionList.module.scss'

export interface ActionItem {
  icon: React.ReactNode
  label: string
  onClick: () => void
  danger?: boolean
}

interface Props {
  triggerRef: RefObject<HTMLElement>
  open: boolean
  onClose?: () => void
  items: ActionItem[]
}

export default function ActionList(props: Props): JSX.Element {
  const { triggerRef, open, onClose, items } = props

  const actionRef = useRef<HTMLDivElement>(null)
  useClickOutside({ actionRef, triggerRef, isActive: open, onClick: () => onClose?.() })

  const handleItemClick = (item: ActionItem) => () => {
    item.onClick()
    onClose?.()
  }

  return (
    <>
      {open && (
        <div ref={actionRef} className={style.action_list}>
          {items.map((item, index) => (
            <button key={index} className={clsx(style.item, item.danger && style.danger)} onClick={handleItemClick(item)}>
              <span className={style.icon}>{item.icon}</span>
              <span>{item.label}</span>
            </button>
          ))}
        </div>
      )}
    </>
  )
}
