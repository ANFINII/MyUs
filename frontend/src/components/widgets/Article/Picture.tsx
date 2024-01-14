import Image from 'next/image'
import Link from 'next/link'
import { Picture } from 'types/internal/media'
import AuthorSpace from 'components/widgets/Common/AuthorSpace'
import ContentTitle from 'components/widgets/Common/ContentTitle'

interface Props {
  data: Picture
}

export default function ArticlePicture(props: Props) {
  const { data } = props
  const { title, image, author, read, like, created } = data

  return (
    <section className="section_list">
      <div className="main_decolation">
        <Link href="/picture/detail/[id][title]">
          <figure>
            <Image src={image} width={272} height={153} alt="" className="radius_10" />
          </figure>
          <div className="author_space">
            <AuthorSpace imageUrl={author.image} nickname={author.nickname} />
            <ContentTitle title={title} nickname={author.nickname} read={read} totalLike={like} created={created} />
          </div>
        </Link>
      </div>
    </section>
  )
}
