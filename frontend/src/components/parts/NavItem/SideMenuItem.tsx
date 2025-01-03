import NavItem from 'components/parts/NavItem'

interface Props {
  label: string
  icon: React.ReactNode
  onClick: () => void
}

export default function SideMenuItem(props: Props) {
  const { label, icon, onClick } = props

  return <NavItem className="side_menu_item" icon={icon} label={label} onClick={onClick} />
}
