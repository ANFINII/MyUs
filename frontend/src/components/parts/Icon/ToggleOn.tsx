interface Props {
  size: string
}

export default function IconToggleOn(props: Props) {
  const { size } = props

  return (
    <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} fill="currentColor" className="bi-toggle-on" viewBox="0 0 16 16">
      <path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10H5zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z" />
    </svg>
  )
}
