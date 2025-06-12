interface Props {
  size: string
  className?: string
}

export default function IconCircle(props: Props): JSX.Element {
  const { size, className = '' } = props

  return (
    <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 16 16" width={size} height={size} className={className}>
      <circle cx="8" cy="8" r="8" />
    </svg>
  )
}
