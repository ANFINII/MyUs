import clsx from 'clsx'
import { ChatDetail } from 'types/internal/media/detail'
import { UserMe } from 'types/internal/user'
import { formatDatetime } from 'utils/functions/datetime'
import AvatarLink from 'components/parts/Avatar/Link'
import Button from 'components/parts/Button'
import IconCaret from 'components/parts/Icon/Caret'
import IconChat from 'components/parts/Icon/Chat'
import IconCross from 'components/parts/Icon/Cross'
import IconDocument from 'components/parts/Icon/Document'
import IconHand from 'components/parts/Icon/Hand'
import IconPerson from 'components/parts/Icon/Person'
import style from './detail.module.scss'

interface Props {
  detail: ChatDetail
  user: UserMe
  subscribeCount: number
  isThread: boolean
  isContent: boolean
  isContentExpand: boolean
  isFallowDisable: boolean
  onContent: () => void
  onContentExpand: () => void
  onLike: () => void
  onModal: () => void
  onSubscribe: () => void
  onThreadClose: () => void
}

export default function SectionHeader(props: Props): React.JSX.Element {
  const { detail, user, subscribeCount, isThread, isContent, isContentExpand, isFallowDisable, onContent, onContentExpand, onLike, onModal, onSubscribe, onThreadClose } = props

  return (
    <>
      <div className={style.chat_section_header}>
        <div className={style.content_toggle} onClick={onContent}>
          <IconDocument size="16" className={style.content_icon} />
          <h1 title={detail.title}>{detail.title}</h1>
        </div>

        {/* コンテンツオーバーレイ */}
        <div className={clsx(style.content_overlay, isContent && style.active)}>
          <div className={style.content_author}>
            <AvatarLink src={detail.channel.avatar} size="m" ulid={detail.channel.ulid} nickname={detail.channel.name} />
            <div className={style.detail}>
              <div className={style.info}>
                <p>{detail.channel.name}</p>
                <time>{formatDatetime(detail.created)}</time>
              </div>
              <div className={style.follower}>
                登録者数 <span>{subscribeCount}</span>
              </div>
            </div>
            <div className={style.follow}>
              {!detail.mediaUser.isSubscribe && <Button color="green" name="チャンネル登録" disabled={isFallowDisable} onClick={onSubscribe} />}
              {detail.mediaUser.isSubscribe && <Button color="white" name="登録済み" onClick={onModal} />}
            </div>
          </div>
          <span className={style.content_expand_toggle} onClick={onContentExpand}>
            {isContentExpand ? '縮小表示' : '拡大表示'}
          </span>
          <div className={clsx(style.content_body, isContentExpand && style.expanded)}>{detail.content}</div>
        </div>

        {/* メディア情報 */}
        <div className={style.media_detail_aria}>
          <span className={style.stat_item}>
            <IconCaret size="14" />
            <span>{detail.read.toLocaleString()}</span>
          </span>
          <span className={style.stat_item}>
            <IconPerson size="14" type="base" />
            <span>{detail.joined.toLocaleString()}</span>
          </span>
          <span className={style.stat_item}>
            <IconChat size="14" />
            <span>{detail.thread.toLocaleString()}</span>
          </span>
          {user.isActive ? (
            <button className={style.like_button} onClick={onLike}>
              <IconHand size="14" type={detail.mediaUser.isLike ? 'on' : 'off'} />
              <span>{detail.like.toLocaleString()}</span>
            </button>
          ) : (
            <span className={style.stat_item}>
              <IconHand size="14" type="off" />
              <span>{detail.like.toLocaleString()}</span>
            </span>
          )}
          <span className={style.stat_item}>
            <time>期間 {formatDatetime(detail.period)}</time>
          </span>
        </div>
      </div>

      {/* スレッドヘッダー */}
      <div className={clsx(style.thread_header, isThread && style.active)}>
        <h2>スレッド</h2>
        <IconCross size="27" onClick={onThreadClose} className={style.thread_close} />
      </div>
    </>
  )
}
