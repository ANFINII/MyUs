import Link from 'next/link'
import config from 'api/config'
import {MediaResponse} from 'utils/type'
import AuthorSpace from 'components/elements/Common/AuthorSpace'
import ContentTitle from 'components/elements/Common/ContentTitle'

interface Props {datas: Array<MediaResponse>}

export default function ArticleCollabo(props: Props) {
  const {datas} = props
  return (
    <article className="article_list">
      {datas.map((data) => {
        const imageUrl = config.baseUrl + data.author.image
        const nickname = data.author.nickname
        return (
          <section className="section_other" key={data.id}>
            <div className="main_decolation">
              <Link href="/collabo/detail/[id][title]" className="author_space">
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
