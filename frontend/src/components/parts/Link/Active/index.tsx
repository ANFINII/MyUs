import Link from 'next/link'
import { useRouter } from 'next/router'

interface Props {
  href: string
  children: React.ReactNode
}

export default function LinkActive(props: Props) {
  const router = useRouter()
  const { href, children } = props

  return (
    <Link href={href} className={router.pathname === href ? 'active' : ''}>
      {children}
    </Link>
  )
}
