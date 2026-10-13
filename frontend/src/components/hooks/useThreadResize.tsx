import { useRef, useCallback, MouseEvent } from 'react'
import { useDragResize } from 'components/hooks/useDragResize'

const THREAD_MIN = 300
const THREAD_MAX_RATIO = 0.6

interface OutProps {
  threadRef: React.RefObject<HTMLDivElement | null>
  resetThreadWidth: () => void
  handleThreadResize: (e: MouseEvent) => void
}

export function useThreadResize(): OutProps {
  const threadRef = useRef<HTMLDivElement>(null)
  const { handleDrag } = useDragResize()

  const resetThreadWidth = useCallback((): void => {
    if (threadRef.current) {
      threadRef.current.style.width = ''
      threadRef.current.style.flex = ''
    }
  }, [])

  const setThreadWidth = useCallback((width: number): void => {
    if (threadRef.current) {
      threadRef.current.style.width = `${width}px`
      threadRef.current.style.flex = 'none'
    }
  }, [])

  const handleThreadResize = useCallback(
    (e: MouseEvent): void => {
      handleDrag(e, (clientX) => {
        const maxWidth = window.innerWidth * THREAD_MAX_RATIO
        setThreadWidth(Math.max(THREAD_MIN, Math.min(window.innerWidth - clientX, maxWidth)))
      })
    },
    [handleDrag, setThreadWidth],
  )

  return { threadRef, resetThreadWidth, handleThreadResize }
}
