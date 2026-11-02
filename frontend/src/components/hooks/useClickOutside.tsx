import { RefObject, useEffect, useEffectEvent } from 'react'

interface Props {
  actionRef: RefObject<HTMLElement | null>
  triggerRef: RefObject<HTMLElement | null>
  isActive?: boolean
  onClick: () => void
}

export function useClickOutside(props: Props): void {
  const { actionRef, triggerRef, isActive, onClick } = props

  const handleClickOutsideEvent = useEffectEvent(() => onClick())

  useEffect(() => {
    if (!isActive) return

    const handleClickOutside = (event: MouseEvent): void => {
      const target = event.target as Node
      const isOutsideRef = actionRef.current && !actionRef.current.contains(target)
      const isOutsideTrigger = !triggerRef.current?.contains(target)
      if (isOutsideRef && isOutsideTrigger) handleClickOutsideEvent()
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [actionRef, triggerRef, isActive])
}
