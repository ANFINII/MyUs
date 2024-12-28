import { useRouter } from 'next/router'
import NavItem from 'components/parts/NavItem'
import ExImage from '../ExImage'
import IconCircle from '../Icon/Circle'

interface Props {
  avatar: string
  nickname: string
  isConfirmed: boolean
  children?: React.ReactNode
  onClick: () => void
}

export default function NotificationItem(props: Props) {
  const { avatar, nickname, isConfirmed, children, onClick } = props

  const router = useRouter()
  const handleRouter = (url: string) => router.push(url)

  return (
    <NavItem className="drop_menu_notification">
      <div className="notification_aria_list">
        <div onClick={() => handleRouter(`/userpage/${nickname}`)}>
          <ExImage src={avatar} title={nickname} className="profile_image" />
        </div>
        {!isConfirmed && <IconCircle size="6" className="svg-circle" />}
        <div className="notification_aria_anker" onClick={onClick}>
          {children}
        </div>
        <form method="POST">
          <i title="閉じる" className="bi-x notification_aria_list_2" style={{ fontSize: '1.41em' }}></i>
        </form>
      </div>
    </NavItem>
  )
}
