interface Props {
  label: string
  icon: React.ReactNode
  onClick: () => void
}

export default function HeaderItem(props: Props): JSX.Element {
  const { label, icon, onClick } = props

  return (
    <li className="drop_menu_list" onClick={onClick}>
      {icon}
      <span>{label}</span>
    </li>
  )
}
