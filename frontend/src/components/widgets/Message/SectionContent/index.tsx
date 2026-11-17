import { useTranslation } from 'react-i18next'
import { ChatDetail } from 'types/internal/media/output'
import { MediaPath } from 'utils/constants/enum'
import cx from 'utils/functions/cx'
import Divide from 'components/parts/Divide'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'
import Advertise from 'components/widgets/Advertise'
import Hashtags from 'components/widgets/Media/Hashtags'
import ProfileInfo from 'components/widgets/ProfileInfo'
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
        <ProfileInfo avatar={channel.avatar} ulid={channel.ownerUlid} name={channel.name} countLabel={t('count.subscribers')} count={subscribeCount} />
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
      <Advertise userUlid={channel.ownerUlid} className={style.advertise} />
    </div>
  )
}
