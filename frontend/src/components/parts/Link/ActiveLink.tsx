import Link from 'next/link'
import {useRouter} from 'next/router'

interface Props {
  children: React.ReactNode
  href: string
}

export default function ActiveLink(props: Props) {
  const router = useRouter()
  const {children, href} = props

  return (
    <Link href={href} className={router.pathname == href ? 'active' : ''}>
      {children}
    </Link>
  )
}
