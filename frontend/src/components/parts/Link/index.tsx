import { MouseEvent } from 'react'
import { useAppRouter } from 'components/hooks/useAppRouter'

interface Props {
  href: string
  className?: string
  children: React.ReactNode
}

export default function Link(props: Props): React.JSX.Element {
  const { href, className, children } = props

  const router = useAppRouter()
  const fullHref = router.locale && href.startsWith('/') ? `/${router.locale}${href}` : href

  const handleClick = (e: MouseEvent<HTMLAnchorElement>) => {
    if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return
    e.preventDefault()
    router.push(href)
  }

  return (
    <a href={fullHref} className={className} onClick={handleClick}>
      {children}
    </a>
  )
}
