interface Props {
  className?: string
}

export default function IconBlockquote(props: Props): React.JSX.Element {
  const { className } = props

  return (
    <svg viewBox="0 0 18 18" className={className}>
      <rect x="3" y="3" width="2" height="12" rx="1" fill="currentColor" stroke="none" />
      <line x1="8" x2="15" y1="5" y2="5" />
      <line x1="8" x2="14" y1="9" y2="9" />
      <line x1="8" x2="13" y1="13" y2="13" />
    </svg>
  )
}
