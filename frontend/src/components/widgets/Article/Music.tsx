import Link from 'next/link'
import { Music } from 'types/internal/media'
import AuthorSpace from 'components/widgets/Common/AuthorSpace'
import ContentTitle from 'components/widgets/Common/ContentTitle'

interface Props {
  data: Music
}

export default function ArticleMusic(props: Props) {
  const { data } = props
  const { author, id, title, music, read, like, created } = data
  const { nickname, avatar } = author

  return (
    <section className="section_music">
      <div className="main_decolation">
        <audio controls controlsList="nodownload" preload="none" className="audio_auto">
          <source src={music} />
          <p>ブラウザがaudioに対応しておりません</p>
        </audio>
        <Link href={`/media/music/${id}`} className="author_space">
          <AuthorSpace imageUrl={avatar} nickname={nickname} />
          <ContentTitle title={title} nickname={nickname} read={read} totalLike={like} created={created} />
        </Link>
      </div>
    </section>
  )
}
