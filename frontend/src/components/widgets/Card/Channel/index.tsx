import { useTranslation } from 'react-i18next'
import { Channel } from 'types/internal/channel'
import ProfileCard from 'components/widgets/Card/Profile'

interface Props {
  item: Channel
}

export default function ChannelCard(props: Props): React.JSX.Element {
  const { item } = props
  const { ulid, ownerUlid, avatar, name, description, count } = item

  const { t } = useTranslation()

  return <ProfileCard href={`/userpage/${ownerUlid}?channel=${ulid}`} avatar={avatar} name={name} counts={[t('count.subscriberCount', { count })]} description={description} />
}
