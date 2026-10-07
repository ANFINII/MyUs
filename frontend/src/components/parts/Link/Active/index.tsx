import { useLocation } from '@tanstack/react-router'
import { isActive } from 'utils/functions/common'
import Link from 'components/parts/Link'

interface Props {
  href: string
  children: React.ReactNode
}

export default function LinkActive(props: Props): React.JSX.Element {
  const { href, children } = props

  const pathname = useLocation({ select: (l) => l.pathname })

  return (
    <Link href={href} className={isActive(pathname === href)}>
      {children}
    </Link>
  )
}
