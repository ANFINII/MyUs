import { useRef, useCallback, MouseEvent } from 'react'

const THREAD_MIN = 300
const THREAD_MAX_RATIO = 0.6

interface OutProps {
  threadRef: React.RefObject<HTMLDivElement | null>
  resetThreadWidth: () => void
  handleThreadResize: (e: MouseEvent) => void
}

export const useThreadResize = (): OutProps => {
  const threadRef = useRef<HTMLDivElement>(null)
  const isDraggingRef = useRef(false)

  const resetThreadWidth = useCallback(() => {
    if (threadRef.current) {
      threadRef.current.style.width = ''
      threadRef.current.style.flex = ''
    }
  }, [])

  const setThreadWidth = useCallback((width: number) => {
    if (threadRef.current) {
      threadRef.current.style.width = `${width}px`
      threadRef.current.style.flex = 'none'
    }
  }, [])

  const handleThreadResize = useCallback(
    (e: MouseEvent) => {
      e.preventDefault()
      isDraggingRef.current = true
      document.body.style.cursor = 'col-resize'
      document.body.style.userSelect = 'none'

      const handleMouseMove = (moveEvent: globalThis.MouseEvent) => {
        if (!isDraggingRef.current) return
        const newWidth = window.innerWidth - moveEvent.clientX
        const maxWidth = window.innerWidth * THREAD_MAX_RATIO
        setThreadWidth(Math.max(THREAD_MIN, Math.min(newWidth, maxWidth)))
      }

      const handleMouseUp = () => {
        isDraggingRef.current = false
        document.body.style.cursor = ''
        document.body.style.userSelect = ''
        document.removeEventListener('mousemove', handleMouseMove)
        document.removeEventListener('mouseup', handleMouseUp)
      }

      document.addEventListener('mousemove', handleMouseMove)
      document.addEventListener('mouseup', handleMouseUp)
    },
    [setThreadWidth],
  )

  return { threadRef, resetThreadWidth, handleThreadResize }
}
