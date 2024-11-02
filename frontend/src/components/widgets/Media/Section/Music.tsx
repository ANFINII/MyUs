import Link from 'next/link'
import { Music } from 'types/internal/media'
import AuthorLink from 'components/parts/AuthorLink'
import ContentTitle from 'components/widgets/Common/ContentTitle'
import style from './Section.module.scss'

interface Props {
  data: Music
}

export default function SectionMusic(props: Props) {
  const { data } = props
  const { author, id, title, music, read, like, created } = data
  const { nickname, avatar } = author

  return (
    <section className={style.section_music}>
      <div className={style.decolation}>
        <audio controls controlsList="nodownload" preload="none" className="audio_auto">
          <source src={music} />
          <p>ブラウザがaudioに対応しておりません</p>
        </audio>
        <Link href={`/media/music/${id}`} className={style.author_space}>
          <AuthorLink imageUrl={avatar} nickname={nickname} />
          <ContentTitle title={title} nickname={nickname} read={read} totalLike={like} created={created} />
        </Link>
      </div>
    </section>
  )
}
