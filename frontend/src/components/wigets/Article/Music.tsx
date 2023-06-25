import Link from 'next/link'
import config from 'api/config'
import {MusicResponse} from 'utils/type'
import AuthorSpace from 'components/wigets/Common/AuthorSpace'
import ContentTitle from 'components/wigets/Common/ContentTitle'

interface Props {data: MusicResponse}

export default function ArticleMusic(props: Props) {
  const {data} = props
  const musicUrl = config.baseUrl + data.music
  const imageUrl = config.baseUrl + data.author.image
  const nickname = data.author.nickname
  return (
    <section className="section_music">
      <div className="main_decolation">
        <audio controls controlsList="nodownload" preload="none" className="audio_auto">
          <source src={musicUrl}/>
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
