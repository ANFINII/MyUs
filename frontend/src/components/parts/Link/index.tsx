import { MouseEvent } from 'react'
import { useLocation, useNavigate } from '@tanstack/react-router'
import { getLocale } from 'lib/i18n'

interface Props {
  href: string
  className?: string
  children: React.ReactNode
}

export default function Link(props: Props): React.JSX.Element {
  const { href, className, children } = props

  const navigate = useNavigate()
  const locale = useLocation({ select: (l) => getLocale(l.publicHref) })
  const fullHref = locale && href.startsWith('/') ? `/${locale}${href}` : href

  const handleClick = (e: MouseEvent<HTMLAnchorElement>) => {
    if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return
    e.preventDefault()
    navigate({ href })
  }

  return (
    <a href={fullHref} className={className} onClick={handleClick}>
      {children}
    </a>
  )
}
