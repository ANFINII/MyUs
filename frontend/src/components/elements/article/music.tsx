import Link from 'next/link'
import config from 'api/config'
import {MusicResponse} from 'utils/type'
import AuthorSpace from 'components/elements/Common/AuthorSpace'
import ContentTitle from 'components/elements/Common/ContentTitle'

interface Props {datas: Array<MusicResponse>}

export default function ArticleMusic(props: Props) {
  const{datas} = props
  return (
    <article className="article_list">
      {datas.map((data) => {
        const imageUrl = config.baseUrl + data.author.image
        const musicUrl = config.baseUrl + data.music
        const nickname = data.author.nickname
        return (
          <section className="section_music" key={data.id}>
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
      })}
    </article>
  )
}
