import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import clsx from 'clsx'
import { Notification, NotificationOut } from 'types/internal/auth'
import { getNotification } from 'api/internal/user'
import { NotificationType } from 'utils/constants/enum'
import { isActive } from 'utils/functions/common'
import { useUser } from 'components/hooks/useUser'
import IconBell from 'components/parts/Icon/Bell'
import DropMenuItem from 'components/parts/NavItem/DropMenuItem'
import NotificationItem from 'components/parts/NavItem/NotificationItem'

interface Props {
  open: boolean
  onClose: () => void
}

const mediaObjs = [NotificationType.Video, NotificationType.Music, NotificationType.Comic, NotificationType.Picture, NotificationType.Blog, NotificationType.Chat]
const otherObjs = [NotificationType.Follow, NotificationType.Like, NotificationType.Reply, NotificationType.Views]

export default function DropMenuNotice(props: Props): JSX.Element {
  const { open, onClose } = props

  const router = useRouter()
  const { user } = useUser()
  const [notifications, setNotifications] = useState<NotificationOut>()

  useEffect(() => {
    if (!user.isActive) return
    const fetch = async () => {
      const ret = await getNotification()
      if (ret.isErr()) return
      setNotifications(ret.value)
    }
    fetch()
  }, [user.isActive])

  const handleRouter = (url: string) => {
    router.push(url)
    onClose()
  }

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
    return (
      threshold && (
        <div className="notification_aria_list_1" title={`${title}が${threshold.message}`}>
          {title}が{threshold.message}
        </div>
      )
    )
  }

  const handleClick = (typeName: NotificationType, notification: Notification) => () => {
    const { contentObject, userFrom } = notification
    if (typeName === NotificationType.Video) handleRouter(`/video/detail/${contentObject.id}`)
    if (typeName === NotificationType.Music) handleRouter(`/music/detail/${contentObject.id}`)
    if (typeName === NotificationType.Comic) handleRouter(`/comic/detail/${contentObject.id}`)
    if (typeName === NotificationType.Picture) handleRouter(`/picture/detail/${contentObject.id}`)
    if (typeName === NotificationType.Blog) handleRouter(`/blog/detail/${contentObject.id}`)
    if (typeName === NotificationType.Chat) handleRouter(`/chat/detail/${contentObject.id}`)
    if (mediaObjs.includes(typeName)) handleRouter(`/userpage/${userFrom.ulid}`)
  }

  return (
    <nav className={clsx('drop_menu', 'drop_menu_notice', isActive(open))}>
      <ul>
        <DropMenuItem label="通知設定" icon={<IconBell size="1.5em" />} onClick={() => handleRouter('/setting/notification')} />
        {notifications?.datas?.map((notification) => {
          const { id, typeName, userFrom, contentObject } = notification
          const { avatar, ulid, nickname } = userFrom
          const { title, text, read } = contentObject
          return (
            <NotificationItem key={id} avatar={avatar} ulid={ulid} nickname={nickname} isConfirmed={notification.isConfirmed} onClick={handleClick(typeName, notification)}>
              <>
                {otherObjs.includes(typeName) && (
                  <div className="notification_aria_list_1" title={`${nickname}が${title}を投稿しました`}>
                    {title}
                  </div>
                )}
                {typeName === NotificationType.Follow && (
                  <div className="notification_aria_list_1" title={`${nickname}にフォローされました`}>
                    {nickname}にフォローされました
                  </div>
                )}
                {typeName === NotificationType.Like && (
                  <div className="notification_aria_list_1" title={`${text}が${nickname}にいいねされました`}>
                    {text}が{nickname}にいいねされました
                  </div>
                )}
                {typeName === NotificationType.Reply && (
                  <div className="notification_aria_list_1" title={`${nickname}から返信がありました ${text}`}>
                    {text}
                  </div>
                )}
                {typeName === NotificationType.Views && <>{readNotification(read, title)}</>}
              </>
            </NotificationItem>
          )
        })}
      </ul>
    </nav>
  )
}
