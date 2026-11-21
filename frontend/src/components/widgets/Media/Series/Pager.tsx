import { useTranslation } from 'react-i18next'
import { Audio, Blog, Comic, MediaSeries, Picture, Video } from 'types/internal/media/output'
import { MediaPath } from 'utils/constants/enum'
import cx from 'utils/functions/cx'
import Link from 'components/parts/Link'
import style from './Pager.module.scss'

type MediaItem = Video | Audio | Blog | Comic | Picture

interface Props {
  series: MediaSeries<MediaItem>
  ulid: string
  mediaPath: MediaPath
  prevLabel: string
  nextLabel: string
  className?: string
}

export default function MediaSeriesPager(props: Props): React.JSX.Element {
  const { series, ulid, mediaPath, prevLabel, nextLabel, className } = props
  const { title, items } = series

  const { t } = useTranslation()

  const index = items.findIndex((item) => item.ulid === ulid)
  if (index === -1 || items.length < 2) return <></>

  const prev = items[index - 1]
  const next = items[index + 1]

  return (
    <nav className={cx(style.pager, className)} aria-label={t('media.series.label')}>
      <div className={style.header}>
        <span className={style.title}>{title}</span>
        <span className={style.position}>{`${index + 1} / ${items.length}`}</span>
      </div>
      <div className={style.links}>
        {prev && (
          <Link href={`/media/${mediaPath}/${prev.ulid}`} className={style.link}>
            <span className={style.direction}>← {prevLabel}</span>
            <span className={style.item_title}>{prev.title}</span>
          </Link>
        )}
        {next && (
          <Link href={`/media/${mediaPath}/${next.ulid}`} className={cx(style.link, style.next)}>
            <span className={style.direction}>{nextLabel} →</span>
            <span className={style.item_title}>{next.title}</span>
          </Link>
        )}
      </div>
    </nav>
  )
}
