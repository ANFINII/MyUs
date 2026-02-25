import clsx from 'clsx'
import { ChatDetail } from 'types/internal/media/detail'
import { UserMe } from 'types/internal/user'
import { formatDatetime } from 'utils/functions/datetime'
import CountLike from 'components/parts/Count/Like'
import IconCaret from 'components/parts/Icon/Caret'
import IconChat from 'components/parts/Icon/Chat'
import IconCross from 'components/parts/Icon/Cross'
import IconDocument from 'components/parts/Icon/Document'
import IconPerson from 'components/parts/Icon/Person'
import HStack from 'components/parts/Stack/Horizontal'
import style from './detail.module.scss'

interface Props {
  detail: ChatDetail
  user: UserMe
  isThread: boolean
  onContent: () => void
  onLike: () => void
  onThreadClose: () => void
}

export default function SectionHeader(props: Props): React.JSX.Element {
  const { detail, user, isThread, onContent, onLike, onThreadClose } = props

  return (
    <>
      <div className={style.chat_section_header}>
        <div className={style.content_toggle} onClick={onContent}>
          <IconDocument size="16" className={style.content_icon} />
          <h1 title={detail.title}>{detail.title}</h1>
        </div>

        <div className={style.media_detail_aria}>
          <HStack gap="4">
            <HStack gap="4" className="rgb100">
              <IconCaret size="14" />
              <span>{detail.read.toLocaleString()}</span>
            </HStack>
            <HStack gap="4" className="rgb100">
              <IconPerson size="14" type="base" />
              <span>{detail.joined.toLocaleString()}</span>
            </HStack>
            <HStack gap="4" className="rgb100">
              <IconChat size="14" />
              <span>{detail.thread.toLocaleString()}</span>
            </HStack>
            <HStack gap="4" className="rgb100">
              <CountLike isLike={detail.mediaUser.isLike} disable={!user.isActive} size="14" count={detail.like} onClick={onLike} />
            </HStack>
            <HStack gap="4" className="rgb100">
              <time>期間 {formatDatetime(detail.period)}</time>
            </HStack>
          </HStack>
        </div>
      </div>

      <div className={clsx(style.thread_header, isThread && style.active)}>
        <h2>スレッド</h2>
        <IconCross size="27" onClick={onThreadClose} className={style.thread_close} />
      </div>
    </>
  )
}
