import { useTranslation } from 'react-i18next'
import { ChannelSeries } from 'types/internal/series'
import CollectionCard from 'components/widgets/Card/Collection'

interface Props {
  item: ChannelSeries
}

export default function SeriesCard(props: Props): React.JSX.Element {
  const { item } = props
  const { title, mediaType, count, mediaUlid, image } = item

  const { t } = useTranslation()

  return <CollectionCard href={`/media/${mediaType.toLowerCase()}/${mediaUlid}`} image={image} count={t('media.series.count', { count })} title={title} sub={mediaType} />
}
