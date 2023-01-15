import Link from 'next/link'
import Image from 'next/image'
import AuthorSpace from 'components/elements/Common/AuthorSpace'
import ContentTitle from 'components/elements/Common/ContentTitle'

interface Props {
  imageUrl: string
  nickname: string
}

export default function ArticleBlog(props: Props) {
  const {imageUrl, nickname} = props
  return (
    <article className="article_list">
      {/* {% for props in blog_list %} */}
      <section className="section_list">
        <figure className="main_decolation">
          <Link href="/blog/detail/[id][title]">
            <Image src={imageUrl} width={272} height={153} alt='' />
          </Link>
          <Link href="/blog/detail/[id][title]" className="author_space">
            <AuthorSpace imageUrl={imageUrl} nickname={nickname} />
            <ContentTitle/>
          </Link>
        </figure>
      </section>
      {/* {% endfor %} */}
    </article>
  )
}
