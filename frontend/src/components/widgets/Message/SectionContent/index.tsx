import { useTranslation } from 'react-i18next'
import { ChatDetail } from 'types/internal/media/output'
import { MediaPath } from 'utils/constants/enum'
import cx from 'utils/functions/cx'
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
  isFollowDisable: boolean
  onModal: () => void
  onSubscribe: () => void
  onContentExpand: () => void
}

export default function SectionContent(props: Props): React.JSX.Element {
  const { detail, subscribeCount, isContent, isContentExpand, isFollowDisable, onModal, onSubscribe, onContentExpand } = props
  const { content, channel, hashtags, mediaUser } = detail

  const { t } = useTranslation()

  return (
    <div className={cx(style.content, isContent && style.active)}>
      {hashtags.length > 0 && (
        <>
          <Hashtags hashtags={hashtags} mediaPath={MediaPath.Chat} />
          <Divide />
        </>
      )}
      <HStack gap="4">
        <AvatarLink size="l" src={channel.avatar} ulid={channel.ownerUlid} title={channel.name} />
        <VStack gap="2">
          <p className="fs_14">{channel.name}</p>
          <HStack gap="4">
            <p className="fs_14 text_sub">
              {t('count.subscribers')}
              <span className="ml_8">{subscribeCount}</span>
            </p>
          </HStack>
        </VStack>
        <div className={style.subscribe}>
          <SubscribeButton isSubscribe={mediaUser.isSubscribe} disabled={isFollowDisable} onModal={onModal} onSubscribe={onSubscribe} />
        </div>
      </HStack>
      <div className={style.content_detail}>
        <VStack gap="2">
          <View isView={isContentExpand} onView={onContentExpand} content={isContentExpand ? t('view.collapse') : t('view.expand')} />
          <div className={cx(style.content_body, isContentExpand && style.active)}>
            <p>{content}</p>
          </div>
        </VStack>
      </div>
    </div>
  )
}
