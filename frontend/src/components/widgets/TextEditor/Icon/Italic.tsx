interface Props {
  className?: string
}

export default function IconItalic(props: Props): React.JSX.Element {
  const { className } = props

  return (
    <svg viewBox="0 0 18 18" className={className}>
      <line x1="7" x2="13" y1="4" y2="4" />
      <line x1="5" x2="11" y1="14" y2="14" />
      <line x1="8" x2="10" y1="14" y2="4" />
    </svg>
  )
}
