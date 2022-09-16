import Head from 'next/head'
import Link from 'next/link'

export default function Follow() {
  return (
    <>
      <Head>
        <title>MyUsフォロワー</title>
      </Head>

      <h1>フォロワー
        {/* {% if query %}
        <section className="messages_search">「{{ query }}」の検索結果「{{ count }}」件</section>
        {% endif %} */}
      </h1>

      {/* {% if user.is_authenticated %} */}
      <div className="follow_button">
        <Link href="/follow/follow" as="/follow">
          <a className="btn btn-primary btn-sm pjax_button" role="button">フォロー</a>
        </Link>
        {/* <span>フォロワー数：{{ user.mypage.follower_num }}</span> */}
      </div>

      <article className="article_list">
        {/* {% for item in follower_list %} */}
        <section className="main_content_follow">
          <div className="main_decolation">
            <Link href="/userpage/[nickname]">
              <a data-name="{{ item.follower.nickname }}" className="author_follows pjax_button_userpage">
                <object className="author_space">
                  <Link href="/userpage/[nickname]">
                    <a data-name="{{ item.follower.nickname }}" className="pjax_button_userpage">
                      {/* <img src="{{ item.follower.image }}" title="{{ item.follower.nickname }}" className="follow_image"> */}
                    </a>
                  </Link>
                </object>
                {/* <span title="{{ item.follower.nickname }}" className="follow_content_1">{{ item.follower.nickname }}</span>
                <span className="follow_content_2">フォロワー数：{{ item.follower.mypage.follower_num }}</span>
                <span className="follow_content_3">フォロー数　：{{ item.follower.mypage.following_num }}</span> */}
                <object title="{{ item.follower.introduction }}" className="follow_content_4">
                  {/* {{ item.follower.introduction|linebreaksbr|urlize }} */}
                </object>
              </a>
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
