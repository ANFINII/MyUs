import Link from 'next/link'
import { Picture } from 'types/internal/media'
import Image from 'components/parts/Image'
import AuthorSpace from 'components/widgets/Common/AuthorSpace'
import ContentTitle from 'components/widgets/Common/ContentTitle'

interface Props {
  data: Picture
}

export default function ArticleBlog(props: Props) {
  const { data } = props
  const { author, id, title, image, read, like, created } = data
  const { nickname } = author

  return (
    <section className="section_list">
      <div className="main_decolation">
        <Link href={`/media/blog/${id}`}>
          <figure>
            <Image src={image} width="272" height="153" alt="" className="radius_8" />
          </figure>
          <div className="author_space">
            <AuthorSpace imageUrl={author.image} nickname={nickname} />
            <ContentTitle title={title} nickname={nickname} read={read} totalLike={like} created={created} />
          </div>
        </Link>
      </div>
    </section>
  )
}
