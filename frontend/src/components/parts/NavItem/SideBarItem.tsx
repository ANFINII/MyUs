import { useRouter } from 'next/router'
import clsx from 'clsx'
import NavItem from 'components/parts/NavItem'

interface Props {
  url: string
  label: string
  icon: React.ReactNode
}

export default function SideBarItem(props: Props): JSX.Element {
  const { url, label, icon } = props

  const router = useRouter()
  const isActive = router.pathname === url
  const handleRouter = () => router.push(url)

  return (
    <NavItem className={clsx('sidebar_color', { active: isActive })}>
      <div onClick={handleRouter}>
        {icon}
        <p className="sidebar_text">{label}</p>
      </div>
    </NavItem>
  )
}
