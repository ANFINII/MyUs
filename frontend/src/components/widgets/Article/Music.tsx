import Link from 'next/link'
import { Music } from 'types/internal/media'
import AuthorSpace from 'components/widgets/Common/AuthorSpace'
import ContentTitle from 'components/widgets/Common/ContentTitle'

interface Props {
  data: Music
}

export default function ArticleMusic(props: Props) {
  const { data } = props

  const musicUrl = data.music
  const imageUrl = data.author.image
  const nickname = data.author.nickname

  return (
    <section className="section_music">
      <div className="main_decolation">
        <audio controls controlsList="nodownload" preload="none" className="audio_auto">
          <source src={musicUrl} />
          <p>ブラウザがaudioに対応しておりません</p>
        </audio>
        <Link href="/music/detail/[id][title]" className="author_space">
          <AuthorSpace imageUrl={imageUrl} nickname={nickname} />
          <ContentTitle title={data.title} nickname={nickname} read={data.read} totalLike={data.like} created={data.created} />
        </Link>
      </div>
    </section>
  )
}
