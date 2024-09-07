import { useRouter } from 'next/router'

interface Props {
  url: string
  label: string
  icon: React.ReactNode
}

export default function HeaderItem(props: Props): JSX.Element {
  const { url, label, icon } = props

  const router = useRouter()
  const handleRouter = () => router.push(url)

  return (
    <li className="drop_menu_list" onClick={handleRouter}>
      {icon}
      <span>{label}</span>
    </li>
  )
}
