const STANDARD_SRC = '/image/logo/myus-logo.svg'
const MIDNIGHT_SRC = '/image/logo/myus-logo-midnight.svg'
const MIDNIGHT_END_HOUR = 6

interface Props {
  className?: string
}

export default function Logo(props: Props): React.JSX.Element {
  const { className } = props

  const src = new Date().getHours() < MIDNIGHT_END_HOUR ? MIDNIGHT_SRC : STANDARD_SRC

  return <img src={src} alt="MyUs" className={className} />
}
