interface Props {
  label: string
  icon: React.ReactNode
  onClick: () => void
}

export default function SideMenuItem(props: Props): JSX.Element {
  const { label, icon, onClick } = props

  return (
    <li className="side_menu_item side_menu_color" onClick={onClick}>
      {icon}
      <span>{label}</span>
    </li>
  )
}
