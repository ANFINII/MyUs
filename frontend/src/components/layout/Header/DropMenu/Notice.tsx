import { useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Notification, NotificationOut } from 'types/internal/user'
import { getNotification, postNotificationConfirmed, postNotificationDeleted } from 'api/internal/user'
import { NotificationType } from 'utils/constants/enum'
import cx from 'utils/functions/cx'
import { useRouter } from 'components/hooks/useRouter'
import { useUser } from 'components/hooks/useUser'
import AvatarLink from 'components/parts/Avatar/Link'
import IconBell from 'components/parts/Icon/Bell'
import IconCircle from 'components/parts/Icon/Circle'
import IconCross from 'components/parts/Icon/Cross'
import NavItem from 'components/parts/NavItem'
import style from './DropMenu.module.scss'

interface Props {
  open: boolean
  onClose: () => void
}

const mediaObjs = [NotificationType.Video, NotificationType.Music, NotificationType.Blog, NotificationType.Comic, NotificationType.Picture, NotificationType.Chat]
const otherObjs = [NotificationType.Follow, NotificationType.Like, NotificationType.Reply, NotificationType.Views]

export default function DropMenuNotice(props: Props): React.JSX.Element {
  const { open, onClose } = props

  const router = useRouter()
  const { t, i18n } = useTranslation()
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
    const thresholds = [10000, 100000, 1000000, 10000000, 100000000, 1000000000]
    const threshold = thresholds.find((limit) => read >= limit)
    if (threshold === undefined) return undefined
    const count = new Intl.NumberFormat(i18n.language, { notation: 'compact' }).format(threshold)
    const message = t('noticeMenu.views', { title, count })
    return (
      <div className={style.content} title={message}>
        {message}
      </div>
    )
  }

  const handleClick = (typeName: NotificationType, notification: Notification) => () => {
    const { ulid, contentObject, userFrom } = notification
    postNotificationConfirmed(ulid)
    setNotifications((prev) => {
      if (prev === undefined) return prev
      return { ...prev, items: prev.items.map((n) => (n.ulid === ulid ? { ...n, isConfirmed: true } : n)) }
    })
    if (typeName === NotificationType.Video) handleRouter(`/media/video/${contentObject.ulid}`)
    if (typeName === NotificationType.Music) handleRouter(`/media/music/${contentObject.ulid}`)
    if (typeName === NotificationType.Blog) handleRouter(`/media/blog/${contentObject.ulid}`)
    if (typeName === NotificationType.Comic) handleRouter(`/media/comic/${contentObject.ulid}`)
    if (typeName === NotificationType.Picture) handleRouter(`/media/picture/${contentObject.ulid}`)
    if (typeName === NotificationType.Chat) handleRouter(`/media/chat/${contentObject.ulid}`)
    if (mediaObjs.includes(typeName)) handleRouter(`/userpage/${userFrom.ulid}`)
  }

  const handleDelete = (ulid: string) => (e: React.MouseEvent) => {
    e.stopPropagation()
    postNotificationDeleted(ulid)
    setNotifications((prev) => {
      if (prev === undefined) return prev
      const items = prev.items.filter((n) => n.ulid !== ulid)
      return { count: items.length, items }
    })
  }

  return (
    <nav className={cx(style.drop_menu, style.drop_menu_notice, open && style.active)}>
      <ul>
        <NavItem label={t('noticeMenu.setting')} icon={<IconBell size="1.5em" />} className={style.item} onClick={() => handleRouter('/setting/notification')} />
        {notifications?.items?.map((notification) => {
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
                    <div className={style.content} title={t('noticeMenu.post', { nickname, title })}>
                      {title}
                    </div>
                  )}
                  {typeName === NotificationType.Follow && (
                    <div className={style.content} title={t('noticeMenu.follow', { nickname })}>
                      {t('noticeMenu.follow', { nickname })}
                    </div>
                  )}
                  {typeName === NotificationType.Like && (
                    <div className={style.content} title={t('noticeMenu.like', { text, nickname })}>
                      {t('noticeMenu.like', { text, nickname })}
                    </div>
                  )}
                  {typeName === NotificationType.Reply && (
                    <div className={style.content} title={t('noticeMenu.reply', { nickname, text })}>
                      {text}
                    </div>
                  )}
                  {typeName === NotificationType.Views && <>{readNotification(read, title)}</>}
                </div>
                <span title={t('noticeMenu.close')} className={style.close} onClick={handleDelete(ulid)}>
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
