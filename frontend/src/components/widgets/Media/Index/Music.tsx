import Link from 'next/link'
import { Music } from 'types/internal/media'
import MediaContent from 'components/widgets/Common/MediaContent'
import style from './Media.module.scss'

interface Props {
  media: Music
}

export default function MediaMusic(props: Props) {
  const { media } = props
  const { id, music } = media

  return (
    <section className={style.media_music}>
      <audio controls controlsList="nodownload" preload="none" className="audio_auto">
        <source src={music} />
        <p>ブラウザがaudioに対応しておりません</p>
      </audio>
      <MediaContent href={`/media/music/${id}`} media={media} />
    </section>
  )
}
