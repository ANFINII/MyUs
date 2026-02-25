import { useRef, useCallback, MouseEvent } from 'react'

const NAV_MIN = 52
const NAV_MAX_RATIO = 0.5
const SIDEBAR_LEFT = 72

interface OutProps {
  navRef: React.RefObject<HTMLDivElement | null>
  handleNavToggle: () => void
  handleResizeStart: (e: MouseEvent) => void
}

export const useNavResize = (): OutProps => {
  const navRef = useRef<HTMLDivElement>(null)
  const navWidthRef = useRef(NAV_MIN)
  const isDraggingRef = useRef(false)

  const setNavWidth = useCallback((width: number) => {
    navWidthRef.current = width
    if (navRef.current) {
      navRef.current.style.width = `${width}px`
    }
  }, [])

  const handleNavToggle = () => {
    const half = (window.innerWidth - SIDEBAR_LEFT) / 2
    setNavWidth(navWidthRef.current > NAV_MIN ? NAV_MIN : half)
  }

  const handleResizeStart = useCallback(
    (e: MouseEvent) => {
      e.preventDefault()
      isDraggingRef.current = true
      document.body.style.cursor = 'col-resize'
      document.body.style.userSelect = 'none'

      const handleMouseMove = (moveEvent: globalThis.MouseEvent) => {
        if (!isDraggingRef.current) return
        const newWidth = moveEvent.clientX - SIDEBAR_LEFT
        const maxWidth = window.innerWidth * NAV_MAX_RATIO
        setNavWidth(Math.max(NAV_MIN, Math.min(newWidth, maxWidth)))
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
    [setNavWidth],
  )

  return { navRef, handleNavToggle, handleResizeStart }
}
