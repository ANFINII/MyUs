interface Props {
  className?: string
  label?: string
  icon?: React.ReactNode
  children?: React.ReactNode
  onClick?: () => void
}

export default function NavItem(props: Props): React.JSX.Element {
  const { className, label, icon, children, onClick } = props

  return (
    <li className={className} onClick={onClick}>
      {icon}
      {label && <span>{label}</span>}
      {children}
    </li>
  )
}
