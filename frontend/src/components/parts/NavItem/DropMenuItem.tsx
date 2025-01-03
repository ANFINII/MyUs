import NavItem from 'components/parts/NavItem'

interface Props {
  label: string
  icon: React.ReactNode
  onClick: () => void
}

export default function DropMenuItem(props: Props) {
  const { label, icon, onClick } = props

  return <NavItem className="drop_menu_list" icon={icon} label={label} onClick={onClick} />
}
