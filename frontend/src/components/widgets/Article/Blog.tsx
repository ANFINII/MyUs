import Image from 'next/image'
import Link from 'next/link'
import config from 'api/config'
import { Picture } from 'types/media'
import AuthorSpace from 'components/widgets/Common/AuthorSpace'
import ContentTitle from 'components/widgets/Common/ContentTitle'

interface Props {
  data: Picture
}

export default function ArticleBlog(props: Props) {
  const { data } = props

  const imageUrl = config.baseUrl + data.image
  const authorUrl = config.baseUrl + data.author.image
  const nickname = data.author.nickname

  return (
    <section className="section_list">
      <Link href="/blog/detail/[id][title]">
        <figure className="main_decolation">
          <Image src={imageUrl} width={272} height={153} alt="" className="radius_10" />
        </figure>
        <div className="author_space">
          <AuthorSpace imageUrl={authorUrl} nickname={nickname} />
          <ContentTitle title={data.title} nickname={nickname} read={data.read} totalLike={data.like} created={data.created} />
        </div>
      </Link>
    </section>
  )
}
