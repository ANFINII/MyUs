import { useCallback, useEffect, useRef, MouseEvent } from 'react'

interface OutProps {
  handleDrag: (e: MouseEvent, onMove: (clientX: number) => void) => void
}

export function useDragResize(): OutProps {
  const cleanupRef = useRef<(() => void) | null>(null)

  // ドラッグ中にアンマウントされたときに、document のリスナーと body のスタイルを戻す
  useEffect(() => {
    return () => cleanupRef.current?.()
  }, [])

  const handleDrag = useCallback((e: MouseEvent, onMove: (clientX: number) => void): void => {
    e.preventDefault()
    document.body.style.cursor = 'col-resize'
    document.body.style.userSelect = 'none'

    const handleMouseMove = (moveEvent: globalThis.MouseEvent): void => onMove(moveEvent.clientX)

    const handleMouseUp = (): void => {
      document.body.style.cursor = ''
      document.body.style.userSelect = ''
      document.removeEventListener('mousemove', handleMouseMove)
      document.removeEventListener('mouseup', handleMouseUp)
      cleanupRef.current = null
    }

    document.addEventListener('mousemove', handleMouseMove)
    document.addEventListener('mouseup', handleMouseUp)
    cleanupRef.current = handleMouseUp
  }, [])

  return { handleDrag }
}
