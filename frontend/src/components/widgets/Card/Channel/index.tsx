import Link from 'next/link'
import { Channel } from 'types/internal/channel'
import ExImage from 'components/parts/ExImage'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'
import style from './Channel.module.scss'

interface Props {
  data: Channel
}

export default function ChannelCard(props: Props): React.JSX.Element {
  const { data } = props
  const { ulid, ownerUlid, avatar, name, description, count } = data

  return (
    <section className={style.media_channel}>
      <Link href={`/userpage/${ownerUlid}?channel=${ulid}`} className={style.channel_box}>
        <HStack gap="5">
          <ExImage src={avatar} title={name} className={style.channel_image} />
          <VStack gap="1" className="fs_12">
            <span title={name}>{name}</span>
            <span>登録者数：{count}</span>
          </VStack>
        </HStack>
        <div title={description} className={style.channel_description}>
          {description}
        </div>
      </Link>
    </section>
  )
}
