import clsx from 'clsx'
import { ChatDetail } from 'types/internal/media/detail'
import { MediaPath } from 'utils/constants/enum'
import AvatarLink from 'components/parts/Avatar/Link'
import Divide from 'components/parts/Divide'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'
import Hashtags from 'components/widgets/Media/Hashtags'
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
  const { content, channel, hashtags, mediaUser } = detail

  return (
    <div className={clsx(style.content, isContent && style.active)}>
      {hashtags.length > 0 && (
        <>
          <Hashtags hashtags={hashtags} mediaPath={MediaPath.Chat} />
          <Divide />
        </>
      )}
      <HStack gap="4" justify="between">
        <HStack gap="4">
          <AvatarLink size="l" src={channel.avatar} ulid={channel.ownerUlid} title={channel.name} />
          <VStack gap="2">
            <p className="fs_14">{channel.name}</p>
            <p className="fs_14 text_sub">
              登録者数<span className="ml_8">{subscribeCount}</span>
            </p>
          </VStack>
        </HStack>
        <div className={style.subscribe}>
          <SubscribeButton isSubscribe={mediaUser.isSubscribe} disabled={isFallowDisable} onModal={onModal} onSubscribe={onSubscribe} />
        </div>
      </HStack>
      <div className={style.content_detail}>
        <VStack gap="2">
          <View isView={isContentExpand} onView={onContentExpand} content={isContentExpand ? '縮小表示' : '拡大表示'} />
          <div className={clsx(style.content_body, isContentExpand && style.active)}>
            <p>{content}</p>
          </div>
        </VStack>
      </div>
    </div>
  )
}
