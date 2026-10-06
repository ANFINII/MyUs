import Link from 'next/link'
import { isActive } from 'utils/functions/common'
import { useAppRouter } from 'components/hooks/useAppRouter'

interface Props {
  href: string
  children: React.ReactNode
}

export default function LinkActive(props: Props): React.JSX.Element {
  const { href, children } = props

  const router = useAppRouter()

  return (
    <Link href={href} className={isActive(router.pathname === href)}>
      {children}
    </Link>
  )
}
