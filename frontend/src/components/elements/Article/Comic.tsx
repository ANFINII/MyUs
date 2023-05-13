import Link from 'next/link'
import {MediaResponse} from 'utils/type'
import config from 'api/config'
import AuthorSpace from 'components/elements/Common/AuthorSpace'
import ContentTitle from 'components/elements/Common/ContentTitle'

interface Props {data: MediaResponse}

export default function ArticleComic(props: Props) {
  const {data} = props
  const imageUrl = config.baseUrl + data.author.image
  const nickname = data.author.nickname
  return (
    <section className="section_other">
      <div className="main_decolation">
        <Link href="/comic/detail/[id][title]" className="author_space">
          <AuthorSpace imageUrl={imageUrl} nickname={nickname} />
          <ContentTitle title={data.title} nickname={nickname} read={data.read} totalLike={data.like} created={data.created} />
        </Link>
      </div>
    </section>
  )
}
