interface Props {
  className?: string
}

export default function IconCodeBlock(props: Props): React.JSX.Element {
  const { className } = props

  return (
    <svg viewBox="0 0 18 18" className={className}>
      <polyline points="5 7 3 9 5 11" />
      <polyline points="13 7 15 9 13 11" />
      <line x1="10" x2="8" y1="5" y2="13" />
    </svg>
  )
}
