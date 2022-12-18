import Head from 'next/head'
import Link from 'next/link'

export default function Follow() {
  return (
    <>
      <Head>
        <title>MyUsフォロー</title>
      </Head>

      <h1>フォロー
        {/* {% if query %}
        <section className="search_message">「{{ query }}」の検索結果「{{ count }}」件</section>
        {% endif %} */}
      </h1>

      {/* {% if user.is_authenticated %} */}
      <div className="follow_button">
        <Link href="/follower" className="btn btn-primary btn-sm pjax_button">フォロワー</Link>
        {/* <span>フォロー数：{{ user.mypage.following_num }}</span> */}
      </div>

      <article className="article_list">
        {/* {% for item in follow_list %} */}
        <section className="section_follow">
          <div className="main_decolation">
            <Link href="/userpage/[nickname]" data-name="{{ item.following.nickname }}" className="author_follows pjax_button_userpage">
              <object className="author_space">
                <Link href="" data-name="{{ item.following.nickname }}" className="pjax_button_userpage">
                  {/* <img src="{{ item.following.image }}" title="{{ item.following.nickname }}" className="follow_image"> */}
                </Link>
              </object>
              {/* <span title="{{ item.following.nickname }}" className="follow_content_1">{{ item.following.nickname }}</span>
              <span className="follow_content_2">フォロワー数：{{ item.following.mypage.follower_num }}</span>
              <span className="follow_content_3">フォロー数　：{{ item.following.mypage.following_num }}</span> */}
              <object title="{{ item.following.introduction }}" className="follow_content_4">
                {/* {{ item.following.introduction|linebreaksbr|urlize }} */}
              </object>
            </Link>
          </div>
        </section>
        {/* {% endfor %} */}
      </article>
      {/* {% else %}
      <h2 className="login_required">ログインしてください</h2>
      {% endif %} */}
    </>
  )
}
