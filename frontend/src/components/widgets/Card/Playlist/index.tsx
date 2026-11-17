import { useTranslation } from 'react-i18next'
import { Playlist } from 'types/internal/playlist'
import IconPlaylist from 'components/parts/Icon/Playlist'
import CollectionCard from 'components/widgets/Card/Collection'

interface Props {
  item: Playlist
}

export default function PlaylistCard(props: Props): React.JSX.Element {
  const { item } = props
  const { ulid, title, publish, count, image } = item

  const { t } = useTranslation()

  return (
    <CollectionCard
      href={`/menu/playlist/${ulid}`}
      image={image}
      icon={<IconPlaylist size="48" />}
      count={t('playlist.count', { count })}
      title={title}
      sub={publish ? t('playlist.public') : t('playlist.private')}
    />
  )
}
