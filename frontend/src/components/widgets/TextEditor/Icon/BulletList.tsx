interface Props {
  className?: string
}

export default function IconBulletList(props: Props): React.JSX.Element {
  const { className } = props

  return (
    <svg viewBox="0 0 18 18" className={className}>
      <line x1="6" x2="15" y1="4" y2="4" />
      <line x1="6" x2="15" y1="9" y2="9" />
      <line x1="6" x2="15" y1="14" y2="14" />
      <line x1="3" x2="3" y1="4" y2="4" />
      <line x1="3" x2="3" y1="9" y2="9" />
      <line x1="3" x2="3" y1="14" y2="14" />
    </svg>
  )
}
