import { isActive } from 'utils/functions/common'
import { useAppRouter } from 'components/hooks/useAppRouter'
import Link from 'components/parts/Link'

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
