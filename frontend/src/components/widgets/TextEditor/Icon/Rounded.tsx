interface Props {
  className?: string
}

export default function IconRounded(props: Props): React.JSX.Element {
  const { className } = props

  return (
    <svg viewBox="0 0 18 18" className={className}>
      <path d="M3 15V8a5 5 0 0 1 5-5h7" />
    </svg>
  )
}
