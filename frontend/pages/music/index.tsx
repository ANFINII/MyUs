import AuthorSpace from 'components/elements/author_space'
import ContentTitle from 'components/elements/content_title'

export default function Music() {
  return (
    <>
      <h1>Music
        {/* {% if query %}
        <section className="messages_search">「{{ query }}」の検索結果「{{ count }}」件</section>
        {% endif %} */}
      </h1>

      <article className="main_article">
        {/* {% for item in music_list %} */}
        <section className="main_content_music">
          <div className="main_decolation">
            <audio controls controlslist="nodownload" preload="none" className="audio_auto">
              <source src="{{ item.music.url }}"/>
              <p>ブラウザがaudioに対応しておりません</p>
            </audio>
            <a href="{% url 'myus:music_detail' item.pk item.title %}" className="author_space">
              <AuthorSpace/>
              <ContentTitle/>
            </a>
          </div>
        </section>
        {/* {% endfor %} */}
      </article>
    </>
  )
}
