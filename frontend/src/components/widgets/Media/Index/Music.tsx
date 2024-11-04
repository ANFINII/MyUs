import Link from 'next/link'
import { Music } from 'types/internal/media'
import MediaContent from 'components/widgets/Common/MediaContent'
import style from './Media.module.scss'

interface Props {
  data: Music
}

export default function MediaMusic(props: Props) {
  const { data } = props
  const { author, id, title, music, read, like, created } = data

  return (
    <section className={style.section_music}>
      <div className={style.decolation}>
        <audio controls controlsList="nodownload" preload="none" className="audio_auto">
          <source src={music} />
          <p>ブラウザがaudioに対応しておりません</p>
        </audio>
        <Link href={`/media/music/${id}`}>
          <MediaContent author={author} title={title} read={read} totalLike={like} created={created} />
        </Link>
      </div>
    </section>
  )
}
