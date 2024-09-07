interface Props {
  label?: string
  icon?: React.ReactNode
  content?: React.ReactNode
  className?: string
  onClick: () => void
}

export default function NavItem(props: Props): JSX.Element {
  const { label, icon, content, className, onClick } = props

  return (
    <li className={className} onClick={onClick}>
      {icon}
      {label && <span>{label}</span>}
      {content}
    </li>
  )
}
