import { useTranslation } from 'react-i18next'
import { ChannelSeries } from 'types/internal/series'
import Card from 'components/parts/Card'
import ExImage from 'components/parts/ExImage'
import Link from 'components/parts/Link'
import style from './Series.module.scss'

interface Props {
  item: ChannelSeries
}

export default function SeriesCard(props: Props): React.JSX.Element {
  const { item } = props
  const { title, mediaType, count, mediaUlid, image } = item

  const { t } = useTranslation()

  return (
    <Card className={style.card}>
      <Link href={`/media/${mediaType.toLowerCase()}/${mediaUlid}`} className={style.link}>
        <div className={style.thumbnail_box}>
          <ExImage src={image} width="195" height="195" className={style.thumbnail} />
          <span className={style.count}>{t('media.series.count', { count })}</span>
        </div>
        <div className={style.content}>
          <div title={title} className={style.title}>
            {title}
          </div>
          <div className={style.media_type}>{mediaType}</div>
        </div>
      </Link>
    </Card>
  )
}
