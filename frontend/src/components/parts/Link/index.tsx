import NextLink from 'next/link'

interface Props {
  href: string
  className?: string
  children: React.ReactNode
}

export default function Link(props: Props): React.JSX.Element {
  const { href, className, children } = props

  return (
    <NextLink href={href} className={className}>
      {children}
    </NextLink>
  )
}
