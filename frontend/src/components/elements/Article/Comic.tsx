import Link from 'next/link'
import Image from 'next/image'
import {ImageResponse} from 'utils/type'
import config from 'api/config'
import AuthorSpace from 'components/elements/Common/AuthorSpace'
import ContentTitle from 'components/elements/Common/ContentTitle'

interface Props {data: ImageResponse}

export default function ArticleComic(props: Props) {
  const {data} = props
  const imageUrl = config.baseUrl + data.image
  const authorUrl = config.baseUrl + data.author.image
  const nickname = data.author.nickname
  return (
    <section className="section_list">
      <Link href="/comic/detail/[id][title]">
        <figure className="main_decolation">
          <Image src={imageUrl} width={272} height={153} alt="" />
        </figure>
        <div className="author_space">
          <AuthorSpace imageUrl={authorUrl} nickname={nickname} />
          <ContentTitle title={data.title} nickname={nickname} read={data.read} totalLike={data.like} created={data.created} />
        </div>
      </Link>
    </section>
  )
}
