import Link from 'next/link'
import Image from 'next/image'
import AuthorSpace from 'components/elements/Common/AuthorSpace'
import ContentTitle from 'components/elements/Common/ContentTitle'

interface Props {imageUrl: string}

export default function PictureArticle(props: Props) {
  const {imageUrl} = props
  return (
    <article className="article_list">
      {/* {% for item in picture_list %} */}
      <section className="section_list">
        <figure className="main_decolation">
          <Link href="/picture/detail/[id][title]">
            <Image src={imageUrl} width={272} height={153} alt="" />
          </Link>
          <Link href="/picture/detail/[id][title]" className="author_space">
            <AuthorSpace imageUrl={imageUrl} />
            <ContentTitle/>
          </Link>
        </figure>
      </section>
      {/* {% endfor %} */}
    </article>
  )
}
