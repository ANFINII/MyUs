import clsx from 'clsx'
import { ChatDetail } from 'types/internal/media/detail'
import { formatDatetime } from 'utils/functions/datetime'
import AvatarLink from 'components/parts/Avatar/Link'
import Button from 'components/parts/Button'
import style from './detail.module.scss'

interface Props {
  detail: ChatDetail
  subscribeCount: number
  isContent: boolean
  isContentExpand: boolean
  isFallowDisable: boolean
  onContent: () => void
  onContentExpand: () => void
  onModal: () => void
  onSubscribe: () => void
}

export default function SectionContent(props: Props): React.JSX.Element {
  const { detail, subscribeCount, isContent, isContentExpand, isFallowDisable, onContent, onContentExpand, onModal, onSubscribe } = props

  return (
    <div className={clsx(style.content_overlay, isContent && style.active)} onClick={onContent}>
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
  )
}
