import { useTranslation } from 'react-i18next'
import { Playlist } from 'types/internal/playlist'
import Card from 'components/parts/Card'
import ExImage from 'components/parts/ExImage'
import IconMusic from 'components/parts/Icon/Music'
import Link from 'components/parts/Link'
import style from './Playlist.module.scss'

interface Props {
  item: Playlist
}

export default function PlaylistCard(props: Props): React.JSX.Element {
  const { item } = props
  const { ulid, title, publish, count, image } = item

  const { t } = useTranslation()

  return (
    <Card className={style.card}>
      <Link href={`/media/music/playlist/${ulid}`} className={style.link}>
        <div className={style.thumbnail_box}>
          {image ? <ExImage src={image} width="195" height="195" className={style.thumbnail} /> : <IconMusic size="48" className={style.icon} />}
          <span className={style.count}>{t('playlist.count', { count })}</span>
        </div>
        <div className={style.content}>
          <div title={title} className={style.title}>
            {title}
          </div>
          <div className={style.publish}>{publish ? t('playlist.public') : t('playlist.private')}</div>
        </div>
      </Link>
    </Card>
  )
}
