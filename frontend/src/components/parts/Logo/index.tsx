import midnightSrc from './myus-logo-midnight.svg'
import standardSrc from './myus-logo.svg'

const MIDNIGHT_END_HOUR = 6

interface Props {
  className?: string
}

export default function Logo(props: Props): React.JSX.Element {
  const { className } = props

  const src = new Date().getHours() < MIDNIGHT_END_HOUR ? midnightSrc : standardSrc

  return <img src={src} alt="MyUs" className={className} />
}
