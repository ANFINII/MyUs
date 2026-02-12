interface Props {
  color: string
  className?: string
}

export default function IconColor(props: Props): React.JSX.Element {
  const { color, className } = props

  return (
    <svg viewBox="0 0 18 18" className={className}>
      <line x1="3" x2="15" y1="15" y2="15" style={{ stroke: color, strokeWidth: 3 }} />
      <polyline points="5.5 11 9 3 12.5 11" />
      <line x1="11.63" x2="6.38" y1="9" y2="9" />
    </svg>
  )
}
