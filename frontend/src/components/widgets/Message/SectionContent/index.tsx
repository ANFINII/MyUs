import clsx from 'clsx'
import { ChatDetail } from 'types/internal/media/detail'
import AvatarLink from 'components/parts/Avatar/Link'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'
import SubscribeButton from 'components/widgets/SubscribeButton'
import View from 'components/widgets/View'
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
      <HStack gap="4" justify="between">
        <HStack gap="4">
          <AvatarLink src={detail.channel.avatar} size="l" ulid={detail.channel.ulid} nickname={detail.channel.name} />
          <VStack gap="2">
            <p className="fs_14">{detail.channel.name}</p>
            <p className="fs_14 text_sub">
              登録者数<span className="ml_8">{subscribeCount}</span>
            </p>
          </VStack>
        </HStack>
        <div className={style.subscribe}>
          <SubscribeButton isSubscribe={detail.mediaUser.isSubscribe} disabled={isFallowDisable} onModal={onModal} onSubscribe={onSubscribe} />
        </div>
      </HStack>
      <div className={style.content_detail}>
        <VStack gap="2">
          <View isView={isContentExpand} onView={onContentExpand} content={isContentExpand ? '縮小表示' : '拡大表示'} />
          <div className={clsx(style.content_body, isContentExpand && style.active_body)}>
            <p>{detail.content}</p>
          </div>
        </VStack>
      </div>
    </div>
  )
}
