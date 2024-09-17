import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import clsx from 'clsx'
import { getNotification } from 'api/internal/user'
import { NotificationOut } from 'types/internal/auth'
import { NotificationType } from 'utils/constants/enum'
import { isActive } from 'utils/functions/common'
import { useUser } from 'components/hooks/useUser'
import ExImage from 'components/parts/ExImage'
import IconBell from 'components/parts/Icon/Bell'
import IconCircle from 'components/parts/Icon/Circle'
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
          <li key={notification.id} className="drop_menu_notification">
            <div className="notification_aria_list">
              <div onClick={() => handleClick(`/userpage/${notification.userFrom.nickname}`)}>
                <ExImage src={notification.userFrom.avatar} title={notification.userFrom.nickname} className="profile_image" />
              </div>

              {!notification.isConfirmed && <IconCircle size="6" className="svg-circle" />}

              {renderElement(
                notification.typeName === NotificationType.Video,
                <div className="notification_aria_anker" onClick={() => handleClick(`/video/detail/${notification.contentObject.id}`)}>
                  <div className="notification_aria_list_1" title={`${notification.userFrom.nickname}さんが${notification.contentObject.title}を投稿しました`}>
                    {notification.contentObject.title}
                  </div>
                </div>,
              )}

              {renderElement(
                notification.typeName === NotificationType.Music,
                <div className="notification_aria_anker" onClick={() => handleClick(`/music/detail/${notification.contentObject.id}`)}>
                  <div className="notification_aria_list_1" title={`${notification.userFrom.nickname}さんが${notification.contentObject.title}を投稿しました`}>
                    {notification.contentObject.title}
                  </div>
                </div>,
              )}

              {renderElement(
                notification.typeName === NotificationType.Comic,
                <div className="notification_aria_anker" onClick={() => handleClick(`/comic/detail/${notification.contentObject.id}`)}>
                  <div className="notification_aria_list_1" title={`${notification.userFrom.nickname}さんが${notification.contentObject.title}を投稿しました`}>
                    {notification.contentObject.title}
                  </div>
                </div>,
              )}

              {renderElement(
                notification.typeName === NotificationType.Picture,
                <div className="notification_aria_anker" onClick={() => handleClick(`/picture/detail/${notification.contentObject.id}`)}>
                  <div className="notification_aria_list_1" title={`${notification.userFrom.nickname}さんが${notification.contentObject.title}を投稿しました`}>
                    {notification.contentObject.title}
                  </div>
                </div>,
              )}

              {renderElement(
                notification.typeName === NotificationType.Blog,
                <div className="notification_aria_anker" onClick={() => handleClick(`/blog/detail/${notification.contentObject.id}`)}>
                  <div className="notification_aria_list_1" title={`${notification.userFrom.nickname}さんが${notification.contentObject.title}を投稿しました`}>
                    {notification.contentObject.title}
                  </div>
                </div>,
              )}

              {renderElement(
                notification.typeName === NotificationType.Chat,
                <div className="notification_aria_anker" onClick={() => handleClick(`/chat/detail/${notification.contentObject.id}`)}>
                  <div className="notification_aria_list_1" title={`${notification.userFrom.nickname}さんが${notification.contentObject.title}を投稿しました`}>
                    {notification.contentObject.title}
                  </div>
                </div>,
              )}

              {notification.typeName === NotificationType.Follow && (
                <div className="notification_aria_anker" onClick={() => handleClick(`/userpage/${notification.userFrom.nickname}`)}>
                  <div className="notification_aria_list_1" title={`${notification.userFrom.nickname}にフォローされました`}>
                    {notification.userFrom.nickname}にフォローされました
                  </div>
                </div>
              )}

              {notification.typeName === NotificationType.Like && (
                <div className="notification_aria_anker" onClick={() => handleClick(`/userpage/${notification.userFrom.nickname}`)}>
                  <div className="notification_aria_list_1" title={`${notification.contentObject.text}が${notification.userFrom.nickname}さんにいいねされました`}>
                    {notification.contentObject.text}が{notification.userFrom.nickname}さんにいいねされました
                  </div>
                </div>
              )}

              {notification.typeName === NotificationType.Reply && (
                <div className="notification_aria_anker" onClick={() => handleClick(`/userpage/${notification.userFrom.nickname}`)}>
                  <div className="notification_aria_list_1" title={`${notification.userFrom.nickname}さんから返信がありました ${notification.contentObject.text}`}>
                    {notification.contentObject.text}
                  </div>
                </div>
              )}

              {notification.typeName === NotificationType.Views && (
                <div className="notification_aria_anker" onClick={() => handleClick(`/userpage/${notification.userFrom.nickname}`)}>
                  {readNotification(notification.contentObject.read, notification.contentObject.title)}
                </div>
              )}

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
