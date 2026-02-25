import clsx from 'clsx'
import { ChatDetail } from 'types/internal/media/detail'
import { UserMe } from 'types/internal/user'
import { formatDatetime } from 'utils/functions/datetime'
import AvatarLink from 'components/parts/Avatar/Link'
import Button from 'components/parts/Button'
import IconCaret from 'components/parts/Icon/Caret'
import IconChat from 'components/parts/Icon/Chat'
import IconCross from 'components/parts/Icon/Cross'
import IconHand from 'components/parts/Icon/Hand'
import IconPerson from 'components/parts/Icon/Person'
import style from './detail.module.scss'

interface Props {
  detail: ChatDetail
  user: UserMe
  joined: number
  thread: number
  likeCount: number
  subscribeCount: number
  isLike: boolean
  isSubscribe: boolean
  isThread: boolean
  isContent: boolean
  isContentExpanded: boolean
  isFallowDisable: boolean
  handleContentToggle: () => void
  handleContentExpand: () => void
  handleLike: () => void
  handleSubscribe: () => void
  handleModal: () => void
  handleThreadClose: () => void
}

export default function SectionHeader(props: Props): React.JSX.Element {
  const {
    detail,
    user,
    joined,
    thread,
    likeCount,
    subscribeCount,
    isLike,
    isSubscribe,
    isThread,
    isContent,
    isContentExpanded,
    isFallowDisable,
    handleContentToggle,
    handleContentExpand,
    handleLike,
    handleSubscribe,
    handleModal,
    handleThreadClose,
  } = props

  return (
    <>
      <div className={style.chat_section_header}>
        <div className={style.content_toggle} onClick={handleContentToggle}>
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" className={style.content_icon} fill="currentColor" viewBox="0 0 16 16">
            <path d="M5 4a.5.5 0 0 0 0 1h6a.5.5 0 0 0 0-1H5zm-.5 2.5A.5.5 0 0 1 5 6h6a.5.5 0 0 1 0 1H5a.5.5 0 0 1-.5-.5zM5 8a.5.5 0 0 0 0 1h6a.5.5 0 0 0 0-1H5zm0 2a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1H5z" />
            <path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2zm10-1H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1z" />
          </svg>
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
              {!isSubscribe && <Button color="green" name="チャンネル登録" disabled={isFallowDisable} onClick={handleSubscribe} />}
              {isSubscribe && <Button color="white" name="登録済み" onClick={handleModal} />}
            </div>
          </div>
          <span className={style.content_expand_toggle} onClick={handleContentExpand}>
            {isContentExpanded ? '縮小表示' : '拡大表示'}
          </span>
          <div className={clsx(style.content_body, isContentExpanded && style.expanded)}>{detail.content}</div>
        </div>

        {/* メディア情報 */}
        <div className={style.media_detail_aria}>
          <span className={style.stat_item}>
            <IconCaret size="14" />
            <span>{detail.read.toLocaleString()}</span>
          </span>
          <span className={style.stat_item}>
            <IconPerson size="14" type="base" />
            <span>{joined.toLocaleString()}</span>
          </span>
          <span className={style.stat_item}>
            <IconChat size="14" />
            <span>{thread.toLocaleString()}</span>
          </span>
          {user.isActive ? (
            <button className={style.like_button} onClick={handleLike}>
              <IconHand size="14" type={isLike ? 'on' : 'off'} />
              <span>{likeCount.toLocaleString()}</span>
            </button>
          ) : (
            <span className={style.stat_item}>
              <IconHand size="14" type="off" />
              <span>{likeCount.toLocaleString()}</span>
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
        <IconCross size="27" onClick={handleThreadClose} className={style.thread_close} />
      </div>
    </>
  )
}
