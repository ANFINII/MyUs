import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import clsx from 'clsx'
import { getNotification } from 'api/internal/user'
import { NotificationOut } from 'types/internal/auth'
import { isActive } from 'utils/functions/common'
import { useUser } from 'components/hooks/useUser'
import ExImage from 'components/parts/ExImage'
import IconBell from 'components/parts/Icon/Bell'
import DropMenuItem from 'components/parts/NavItem/DropMenuItem'

interface Props {
  open: boolean
  onClose: () => void
}

export default function DropMenuNotice(props: Props) {
  const { open, onClose } = props

  const router = useRouter()
  const { user } = useUser()
  const [notifications, setNotifications] = useState<NotificationOut>()

  useEffect(() => {
    if (!user.isActive) return
    const fetch = async () => {
      const notifications = await getNotification()
      setNotifications(notifications)
    }
    fetch()
  }, [user.isActive])

  const handleClick = (url: string) => {
    router.push(url)
    onClose()
  }

  const renderElement = (isBool: boolean, element: JSX.Element) => isBool && element

  const readNotification = (read: number, title: string) => {
    const thresholds = [
      { limit: 10000, message: '1万回閲覧されました' },
      { limit: 100000, message: '10万回閲覧されました' },
      { limit: 1000000, message: '100万回閲覧されました' },
      { limit: 10000000, message: '1000万回閲覧されました' },
      { limit: 100000000, message: '1億回閲覧されました' },
      { limit: 1000000000, message: '10億回閲覧されました' },
    ]
    const threshold = thresholds.find((t) => read >= t.limit)
    return threshold ? (
      <div className="notification_aria_list_1" title={`${title}が${threshold.message}`}>
        {title}が{threshold.message}
      </div>
    ) : (
      <></>
    )
  }

  return (
    <nav className={clsx('drop_menu drop_menu_notice', isActive(open))}>
      <ul>
        <DropMenuItem label="通知設定" icon={<IconBell size="1.5em" />} onClick={() => handleClick('/setting/notification')} />
        {notifications?.datas?.map((notification) => (
          <li key={notification.id} className="drop_menu_list">
            <div className="notification_aria_list">
              <a onClick={() => handleClick(`/userpage/${notification.userFrom.nickname}`)}>
                <ExImage src={notification.userFrom.avatar} title={notification.userFrom.nickname} className="profile_image" />
              </a>
              {!notification.isConfirmed && (
                <svg xmlns="http://www.w3.org/2000/svg" className="svg-circle" viewBox="0 0 2 2">
                  <circle cx="1" cy="1" r="1"></circle>
                </svg>
              )}
              {renderElement(notification.typeName === 'video', <a className="notification_aria_anker" onClick={() => handleClick(`/video/detail/${notification.contentObject.id}`)} />)}
              {renderElement(notification.typeName === 'music', <a className="notification_aria_anker" onClick={() => handleClick(`/music/detail/${notification.contentObject.id}`)} />)}
              {renderElement(notification.typeName === 'comic', <a className="notification_aria_anker" onClick={() => handleClick(`/comic/detail/${notification.contentObject.id}`)} />)}
              {renderElement(notification.typeName === 'picture', <a className="notification_aria_anker" onClick={() => handleClick(`/picture/detail/${notification.contentObject.id}`)} />)}
              {renderElement(notification.typeName === 'blog', <a className="notification_aria_anker" onClick={() => handleClick(`/blog/detail/${notification.contentObject.id}`)} />)}
              {renderElement(notification.typeName === 'chat', <a className="notification_aria_anker" onClick={() => handleClick(`/chat/detail/${notification.contentObject.id}`)} />)}
              {notification.typeNo >= 8 && notification.typeNo <= 10 && <a className="notification_aria_anker" onClick={() => handleClick(`/chat/detail/${notification.userFrom.nickname}`)} />}
              {notification.typeNo >= 1 && notification.typeNo <= 7 && (
                <div className="notification_aria_list_1" title={`${notification.userFrom.nickname}さんが${notification.contentObject.title}を投稿しました`}>
                  {notification.contentObject.title}
                </div>
              )}
              {notification.typeNo === 7 && (
                <div className="notification_aria_list_1" title={`${notification.userFrom.nickname}にフォローされました`}>
                  {notification.userFrom.nickname}にフォローされました
                </div>
              )}
              {notification.typeNo === 8 && (
                <div className="notification_aria_list_1" title={`${notification.contentObject.text}が${notification.userFrom.nickname}さんにいいねされました`}>
                  {notification.contentObject.text}が{notification.userFrom.nickname}さんにいいねされました
                </div>
              )}
              {notification.typeNo === 9 && (
                <div className="notification_aria_list_1" title={`${notification.userFrom.nickname}さんから返信がありました ${notification.contentObject.text}`}>
                  {notification.contentObject.text}
                </div>
              )}
              {(notification.typeNo === 10, readNotification(notification.contentObject.read, notification.contentObject.title))}
              <form method="POST">
                <i title="閉じる" className="bi-x notification_aria_list_2" style={{ fontSize: '1.41em' }}></i>
              </form>
            </div>
          </li>
        ))}
      </ul>
    </nav>
  )
}
