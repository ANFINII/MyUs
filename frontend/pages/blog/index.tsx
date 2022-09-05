import AuthorSpace from 'components/elements/author_space'
import ContentTitle from 'components/elements/content_title'

export default function Blog(props) {
  return (
    <>
      <h1>Blog
        {/* if (props.query) { */}
          <section className="messages_search">「{ props.query }」の検索結果「{ props.count }」件</section>
        {/* } */}
      </h1>

      <article className="main_article">
        {/* {% for props in blog_list %} */}
        <section className="main_content">
          <figure className="main_decolation">
            <a href="{% url 'myus:blog_detail' props.pk props.title %}">
              <img src="{{ props.image.url }}" width="272" height="153"/>
            </a>
            <a href="{% url 'myus:blog_detail' props.pk props.title %}" className="author_space">
              <AuthorSpace/>
              <ContentTitle/>
            </a>
          </figure>
        </section>
        {/* {% endfor %} */}
      </article>
    </>
  )
}
