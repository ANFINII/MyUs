import Link from 'next/link'
import { useRouter } from 'next/router'
import { isActive } from 'utils/functions/common'

interface Props {
  href: string
  children: React.ReactNode
}

export default function LinkActive(props: Props) {
  const router = useRouter()
  const { href, children } = props

  return (
    <Link href={href} className={isActive(router.pathname === href)}>
      {children}
    </Link>
  )
}
