import { useTranslation } from 'react-i18next'
import { Follow } from 'types/internal/user'
import ProfileCard from 'components/widgets/Card/Profile'

interface Props {
  item: Follow
}

export default function FollowCard(props: Props): React.JSX.Element {
  const { item } = props
  const { avatar, ulid, nickname, introduction, followerCount, followingCount } = item

  const { t } = useTranslation()

  const counts = [t('count.followers', { count: followerCount }), t('count.following', { count: followingCount })]

  return <ProfileCard href={`/userpage/${ulid}`} avatar={avatar} name={nickname} counts={counts} description={introduction} />
}
