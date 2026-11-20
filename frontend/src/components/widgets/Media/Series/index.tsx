import { useTranslation } from 'react-i18next'
import { Blog, Chat, Comic, MediaSeries, Audio, Picture, Video } from 'types/internal/media/output'
import { MediaPath } from 'utils/constants/enum'
import cx from 'utils/functions/cx'
import ExImage from 'components/parts/ExImage'
import Link from 'components/parts/Link'
import style from './Series.module.scss'

type MediaItem = Video | Audio | Blog | Comic | Picture | Chat

const thumbnail = (item: MediaItem): string => ('image' in item && item.image) || item.channel.avatar

interface Props {
  series: MediaSeries<MediaItem>
  ulid: string
  mediaPath: MediaPath
  className?: string
}

export default function MediaDetailSeries(props: Props): React.JSX.Element {
  const { series, ulid, mediaPath, className } = props
  const { title, items } = series

  const { t } = useTranslation()

  if (items.length === 0) return <></>

  const index = items.findIndex((item) => item.ulid === ulid)

  return (
    <section className={cx(style.series, className)}>
      <div className={style.header}>
        <span className={style.label}>{t('media.series.label')}</span>
        <span className={style.title}>{title}</span>
        <span className={style.position}>{`${index + 1} / ${items.length}`}</span>
      </div>
      <ol className={style.list}>
        {items.map((item, i) => (
          <li key={item.ulid}>
            <Link href={`/media/${mediaPath}/${item.ulid}`} className={cx(style.item, item.ulid === ulid && style.current)}>
              <span className={style.index}>{i + 1}</span>
              <ExImage src={thumbnail(item)} className={style.thumbnail} />
              <span className={style.item_title}>{item.title}</span>
            </Link>
          </li>
        ))}
      </ol>
    </section>
  )
}
