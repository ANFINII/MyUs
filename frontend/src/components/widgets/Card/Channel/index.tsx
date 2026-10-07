import { useTranslation } from 'react-i18next'
import { Channel } from 'types/internal/channel'
import Card from 'components/parts/Card'
import ExImage from 'components/parts/ExImage'
import Link from 'components/parts/Link'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'
import style from './Channel.module.scss'

interface Props {
  item: Channel
}

export default function ChannelCard(props: Props): React.JSX.Element {
  const { item } = props
  const { ulid, ownerUlid, avatar, name, description, count } = item

  const { t } = useTranslation()

  return (
    <Card className={style.card}>
      <Link href={`/userpage/${ownerUlid}?channel=${ulid}`} className={style.box}>
        <HStack gap="5">
          <ExImage src={avatar} title={name} className={style.image} />
          <VStack gap="1" className="fs_12">
            <span title={name}>{name}</span>
            <span>{t('count.subscriberCount', { count })}</span>
          </VStack>
        </HStack>
        <div title={description} className={style.description}>
          {description}
        </div>
      </Link>
    </Card>
  )
}
