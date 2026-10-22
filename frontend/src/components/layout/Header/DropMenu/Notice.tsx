import { useTranslation } from 'react-i18next'
import { useQueryClient } from '@tanstack/react-query'
import { toErrorMessage } from 'lib/error'
import { queryKeys } from 'lib/query/keys'
import { Notification, NotificationOut } from 'types/internal/user'
import { postNotificationConfirmed, postNotificationDeleted } from 'api/internal/user'
import { FetchError, MediaPath, MediaType, NotificationType } from 'utils/constants/enum'
import cx from 'utils/functions/cx'
import { useRouter } from 'components/hooks/useRouter'
import { useToast } from 'components/hooks/useToast'
import AvatarLink from 'components/parts/Avatar/Link'
import IconBell from 'components/parts/Icon/Bell'
import IconCircle from 'components/parts/Icon/Circle'
import IconCross from 'components/parts/Icon/Cross'
import NavItem from 'components/parts/NavItem'
import Toast from 'components/parts/Toast'
import style from './DropMenu.module.scss'

interface Props {
  open: boolean
  notifications?: NotificationOut
  onClose: () => void
}

const mediaObjs = [NotificationType.Video, NotificationType.Music, NotificationType.Blog, NotificationType.Comic, NotificationType.Picture, NotificationType.Chat]
const mediaPaths: Record<MediaType, MediaPath> = {
  [MediaType.Video]: MediaPath.Video,
  [MediaType.Music]: MediaPath.Music,
  [MediaType.Blog]: MediaPath.Blog,
  [MediaType.Comic]: MediaPath.Comic,
  [MediaType.Picture]: MediaPath.Picture,
  [MediaType.Chat]: MediaPath.Chat,
}

export default function DropMenuNotice(props: Props): React.JSX.Element {
  const { open, notifications, onClose } = props

  const router = useRouter()
  const queryClient = useQueryClient()
  const { t, i18n } = useTranslation()
  const { toast, handleToast } = useToast()

  const updateNotifications = (update: (prev: NotificationOut) => NotificationOut): void => {
    queryClient.setQueryData<NotificationOut>(queryKeys.notification, (prev) => prev && update(prev))
  }

  const handleRouter = (url: string) => {
    router.push(url)
    onClose()
  }

  const readNotification = (read: number, title: string) => {
    const thresholds = [10000, 100000, 1000000, 10000000, 100000000, 1000000000]
    const threshold = thresholds.findLast((limit) => read >= limit)
    if (threshold === undefined) return undefined
    const count = new Intl.NumberFormat(i18n.language, { notation: 'compact' }).format(threshold)
    const message = t('noticeMenu.views', { title, count })
    return (
      <div className={style.content} title={message}>
        {message}
      </div>
    )
  }

  const handleClick = (notification: Notification) => async () => {
    const { ulid, contentObject, userFrom, isConfirmed } = notification
    const { mediaType, mediaUlid, threadUlid } = contentObject
    updateNotifications((prev) => ({
      count: isConfirmed ? prev.count : prev.count - 1,
      items: prev.items.map((n) => (n.ulid === ulid ? { ...n, isConfirmed: true } : n)),
    }))
    if (mediaType === null) handleRouter(`/userpage/${userFrom.ulid}`)
    else if (threadUlid) handleRouter(`/media/${mediaPaths[mediaType]}/${mediaUlid}/thread/${threadUlid}`)
    else handleRouter(`/media/${mediaPaths[mediaType]}/${mediaUlid}`)
    const ret = await postNotificationConfirmed(ulid)
    if (ret.isErr()) handleToast(toErrorMessage(ret.error, FetchError.Post), true)
  }

  const handleDelete = (notification: Notification) => async (e: React.MouseEvent) => {
    const { ulid, isConfirmed } = notification
    e.stopPropagation()
    updateNotifications((prev) => ({
      count: isConfirmed ? prev.count : prev.count - 1,
      items: prev.items.filter((n) => n.ulid !== ulid),
    }))
    const ret = await postNotificationDeleted(ulid)
    if (ret.isErr()) handleToast(toErrorMessage(ret.error, FetchError.Delete), true)
  }

  return (
    <>
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
                  <div className={style.anker} onClick={handleClick(notification)}>
                    {mediaObjs.includes(typeName) && (
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
                  <span title={t('noticeMenu.close')} className={style.close} onClick={handleDelete(notification)}>
                    <IconCross size="18" className={style.close_icon} />
                  </span>
                </div>
              </NavItem>
            )
          })}
        </ul>
      </nav>
      <Toast {...toast} />
    </>
  )
}
