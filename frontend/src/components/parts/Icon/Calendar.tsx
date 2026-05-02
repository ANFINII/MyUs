interface Props {
  size: string
  className?: string
}

export default function IconCalendar(props: Props): React.JSX.Element {
  const { size, className } = props

  return (
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" strokeWidth="1.5" viewBox="0 0 16 16" width={size} height={size} className={className}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M5 1v2M11 1v2M2 6h12M3 3h10a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1z" />
    </svg>
  )
}
