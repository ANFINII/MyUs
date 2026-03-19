import NavItem from 'components/parts/NavItem'

interface Props {
  label: string
  icon: React.ReactNode
  className?: string
  onClick: () => void
}

export default function SideBarItem(props: Props): React.JSX.Element {
  const { label, icon, className, onClick } = props

  return (
    <NavItem className={className} onClick={onClick}>
      <div>
        {icon}
        <p>{label}</p>
      </div>
    </NavItem>
  )
}
