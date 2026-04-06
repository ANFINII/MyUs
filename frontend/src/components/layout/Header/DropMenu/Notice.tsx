import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import { Notification, NotificationOut } from 'types/internal/user'
import { getNotification, postNotificationConfirmed, postNotificationDeleted } from 'api/internal/user'
import { NotificationType } from 'utils/constants/enum'
import cx from 'utils/functions/cx'
import { useUser } from 'components/hooks/useUser'
import AvatarLink from 'components/parts/Avatar/Link'
import IconBell from 'components/parts/Icon/Bell'
import IconCircle from 'components/parts/Icon/Circle'
import IconCross from 'components/parts/Icon/Cross'
import NavItem from 'components/parts/NavItem'
import MenuItem from 'components/parts/NavItem/MenuItem'
import style from './DropMenu.module.scss'

interface Props {
  open: boolean
  onClose: () => void
}

const mediaObjs = [NotificationType.Video, NotificationType.Music, NotificationType.Comic, NotificationType.Picture, NotificationType.Blog, NotificationType.Chat]
const otherObjs = [NotificationType.Follow, NotificationType.Like, NotificationType.Reply, NotificationType.Views]

export default function DropMenuNotice(props: Props): React.JSX.Element {
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
        <div className={style.content} title={`${title}が${threshold.message}`}>
          {title}が{threshold.message}
        </div>
      )
    )
  }

  const handleClick = (typeName: NotificationType, notification: Notification) => () => {
    const { ulid, contentObject, userFrom } = notification
    postNotificationConfirmed(ulid)
    setNotifications((prev) => {
      if (prev === undefined) return prev
      return { ...prev, datas: prev.datas.map((n) => (n.ulid === ulid ? { ...n, isConfirmed: true } : n)) }
    })
    if (typeName === NotificationType.Video) handleRouter(`/video/detail/${contentObject.id}`)
    if (typeName === NotificationType.Music) handleRouter(`/music/detail/${contentObject.id}`)
    if (typeName === NotificationType.Comic) handleRouter(`/comic/detail/${contentObject.id}`)
    if (typeName === NotificationType.Picture) handleRouter(`/picture/detail/${contentObject.id}`)
    if (typeName === NotificationType.Blog) handleRouter(`/blog/detail/${contentObject.id}`)
    if (typeName === NotificationType.Chat) handleRouter(`/chat/detail/${contentObject.id}`)
    if (mediaObjs.includes(typeName)) handleRouter(`/userpage/${userFrom.ulid}`)
  }

  const handleDelete = (ulid: string) => (e: React.MouseEvent) => {
    e.stopPropagation()
    postNotificationDeleted(ulid)
    setNotifications((prev) => {
      if (prev === undefined) return prev
      const datas = prev.datas.filter((n) => n.ulid !== ulid)
      return { count: datas.length, datas }
    })
  }

  return (
    <nav className={cx(style.drop_menu, style.drop_menu_notice, open && style.active)}>
      <ul>
        <MenuItem label="通知設定" icon={<IconBell size="1.5em" />} className={style.item} onClick={() => handleRouter('/setting/notification')} />
        {notifications?.datas?.map((notification) => {
          const { ulid, typeName, userFrom, contentObject, isConfirmed } = notification
          const { avatar, nickname } = userFrom
          const { title, text, read } = contentObject
          return (
            <NavItem key={ulid}>
              <div className={style.notice_item}>
                <div className={style.avatar}>
                  <AvatarLink src={avatar} ulid={userFrom.ulid} title={nickname} size="s" />
                  <IconCircle size="6" className={isConfirmed ? style.hidden : style.circle} />
                </div>
                <div className={style.anker} onClick={handleClick(typeName, notification)}>
                  {otherObjs.includes(typeName) && (
                    <div className={style.content} title={`${nickname}が${title}を投稿しました`}>
                      {title}
                    </div>
                  )}
                  {typeName === NotificationType.Follow && (
                    <div className={style.content} title={`${nickname}にフォローされました`}>
                      {nickname}にフォローされました
                    </div>
                  )}
                  {typeName === NotificationType.Like && (
                    <div className={style.content} title={`${text}が${nickname}にいいねされました`}>
                      {text}が{nickname}にいいねされました
                    </div>
                  )}
                  {typeName === NotificationType.Reply && (
                    <div className={style.content} title={`${nickname}から返信がありました ${text}`}>
                      {text}
                    </div>
                  )}
                  {typeName === NotificationType.Views && <>{readNotification(read, title)}</>}
                </div>
                <span title="閉じる" className={style.close} onClick={handleDelete(ulid)}>
                  <IconCross size="18" className={style.close_icon} />
                </span>
              </div>
            </NavItem>
          )
        })}
      </ul>
    </nav>
  )
}
