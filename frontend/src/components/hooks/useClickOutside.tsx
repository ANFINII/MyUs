import { RefObject, useEffect } from 'react'

interface Props {
  actionRef: RefObject<HTMLElement>
  triggerRef?: RefObject<HTMLElement>
  isActive?: boolean
  onClick: () => void
}

export function useClickOutside(props: Props): void {
  const { actionRef, triggerRef, isActive, onClick } = props

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (!isActive) return
      const target = event.target as Node
      const isOutsideRef = actionRef.current && !actionRef.current.contains(target)
      const isOutsideTrigger = triggerRef?.current ? !triggerRef.current.contains(target) : true
      if (isOutsideRef && isOutsideTrigger) onClick()
    }

    if (isActive) {
      document.addEventListener('mousedown', handleClickOutside)
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [actionRef, triggerRef, isActive, onClick])
}
