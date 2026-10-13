import { useRef, useCallback, MouseEvent } from 'react'
import { useDragResize } from 'components/hooks/useDragResize'

const NAV_MIN = 52
const NAV_MAX_RATIO = 0.5
const SIDEBAR_LEFT = 72

interface OutProps {
  navRef: React.RefObject<HTMLDivElement | null>
  handleNav: () => void
  handleResize: (e: MouseEvent) => void
}

export function useNavResize(): OutProps {
  const navRef = useRef<HTMLDivElement>(null)
  const navWidthRef = useRef<number>(NAV_MIN)
  const { handleDrag } = useDragResize()

  const setNavWidth = useCallback((width: number): void => {
    navWidthRef.current = width
    if (navRef.current) {
      navRef.current.style.width = `${width}px`
    }
  }, [])

  const handleNav = (): void => {
    const half = (window.innerWidth - SIDEBAR_LEFT) / 2
    setNavWidth(navWidthRef.current > NAV_MIN ? NAV_MIN : half)
  }

  const handleResize = useCallback(
    (e: MouseEvent): void => {
      handleDrag(e, (clientX) => {
        const maxWidth = window.innerWidth * NAV_MAX_RATIO
        setNavWidth(Math.max(NAV_MIN, Math.min(clientX - SIDEBAR_LEFT, maxWidth)))
      })
    },
    [handleDrag, setNavWidth],
  )

  return { navRef, handleNav, handleResize }
}
