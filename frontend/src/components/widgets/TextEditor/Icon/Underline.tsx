interface Props {
  className?: string
}

export default function IconUnderline(props: Props): React.JSX.Element {
  const { className } = props

  return (
    <svg viewBox="0 0 18 18" className={className}>
      <path d="M5,3V9a4.012,4.012,0,0,0,4,4H9a4.012,4.012,0,0,0,4-4V3" />
      <rect height="1" rx="0.5" ry="0.5" width="12" x="3" y="15" fill="currentColor" stroke="none" />
    </svg>
  )
}
