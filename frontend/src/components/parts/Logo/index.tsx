interface Props {
  height: string
  className?: string
}

export default function Logo(props: Props): React.JSX.Element {
  const { height, className } = props

  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="1 5 70 24"
      height={height}
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
      role="img"
      aria-label="MyUs"
      className={className}
    >
      <path d="M2 22V6l8.5 11L19 6v16" />
      <path d="M24 11l5.5 11M35 11l-7 14.5c-1 2-2.4 2.7-4.5 2.3" />
      <path d="M40 6v9.5a7 7 0 0 0 14 0V6" />
      <path d="M68.5 12.6c-.9-1.2-2.4-1.9-4.2-1.9-2.4 0-4 1.2-4 3s1.4 2.5 4.1 3c2.9.5 4.4 1.4 4.4 3.4s-1.8 3.2-4.4 3.2c-2 0-3.7-.8-4.6-2.1" />
    </svg>
  )
}
