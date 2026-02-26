import clsx from 'clsx'
import { ChatDetail } from 'types/internal/media/detail'
import { formatDatetime } from 'utils/functions/datetime'
import AvatarLink from 'components/parts/Avatar/Link'
import SubscribeButton from 'components/widgets/SubscribeButton'
import style from './SectionContent.module.scss'

interface Props {
  detail: ChatDetail
  subscribeCount: number
  isContent: boolean
  isContentExpand: boolean
  isFallowDisable: boolean
  onModal: () => void
  onSubscribe: () => void
  onContentExpand: () => void
}

export default function SectionContent(props: Props): React.JSX.Element {
  const { detail, subscribeCount, isContent, isContentExpand, isFallowDisable, onModal, onSubscribe, onContentExpand } = props

  return (
    <div className={clsx(style.content_overlay, isContent && style.active)}>
      <div className={style.content_author}>
        <AvatarLink src={detail.channel.avatar} size="m" ulid={detail.channel.ulid} nickname={detail.channel.name} />
        <div className={style.detail}>
          <div className={style.info}>
            <p>{detail.channel.name}</p>
            <time>{formatDatetime(detail.created)}</time>
          </div>
          <div className={style.subscribe_count}>
            登録者数 <span>{subscribeCount}</span>
          </div>
        </div>
        <div className={style.subscribe}>
          <SubscribeButton isSubscribe={detail.mediaUser.isSubscribe} disabled={isFallowDisable} onModal={onModal} onSubscribe={onSubscribe} />
        </div>
      </div>
      <span className={style.content_expand_toggle} onClick={onContentExpand}>
        {isContentExpand ? '縮小表示' : '拡大表示'}
      </span>
      <div className={clsx(style.content_body, isContentExpand && style.expanded)}>{detail.content}</div>
    </div>
  )
}
