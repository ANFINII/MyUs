import NavItem from 'components/parts/NavItem'

interface Props {
  label: string
  icon: React.ReactNode
  className?: string
  onClick: () => void
}

export default function MenuItem(props: Props): React.JSX.Element {
  const { label, icon, className, onClick } = props

  return <NavItem icon={icon} label={label} className={className} onClick={onClick} />
}
