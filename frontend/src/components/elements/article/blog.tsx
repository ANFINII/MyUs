import Link from 'next/link'
import AuthorSpace from 'components/elements/common/author_space'
import ContentTitle from 'components/elements/common/content_title'
import Image from 'next/image'

interface Props {
  imageUrl: string
}

export default function BlogArticle(props: Props) {
  const { imageUrl } = props
  return (
    <article className="article_list">
      {/* {% for props in blog_list %} */}
      <section className="section_list">
        <figure className="main_decolation">
          <Link href="/blog/detail/[id][title]">
            <Image src={imageUrl} width={272} height={153} alt=''/>
          </Link>
          <Link href="/blog/detail/[id][title]" className="author_space">
            <AuthorSpace/>
            <ContentTitle/>
          </Link>
        </figure>
      </section>
      {/* {% endfor %} */}
    </article>
  )
}
