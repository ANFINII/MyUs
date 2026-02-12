interface Props {
  className?: string
}

export default function IconImage(props: Props): React.JSX.Element {
  const { className } = props

  return (
    <svg viewBox="0 0 28 20" className={className}>
      <rect x="2" y="2" width="24" height="16" rx="2" ry="2" />
      <circle cx="8" cy="7.5" r="1.5" />
      <polyline points="26 14 20 8 8 18" />
    </svg>
  )
}
