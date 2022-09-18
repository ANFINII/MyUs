import Head from 'next/head'
import Footer from 'components/layouts/footer'

export default function Profile() {
  return (
    <>
      <Head>
        <title>MyUsアカウント設定</title>
      </Head>

      <article className="article_account">
        <h1>アカウント設定</h1>
        {/* {% if user.is_authenticated %} */}
        <div className="btn-column">
          <div className="btn-column1">
            <a href="{% url 'myus:profile_update' %}" className="btn btn-success btn-sm" role="button">編集</a>
          </div>
          <div className="btn-column2">
            <a href="{% url 'password_change' %}" className="btn btn-success btn-sm" role="button">パスワード変更</a>
          </div>
        </div>

        <table>
          <tbody>
            <tr><td className="td-color td-header">アカウント画像</td>
              <td>
                <label htmlFor="account_image_input" className="account_image">
                  <a href="{{ user.image }}" data-lightbox="group">
                    <img src="{{ user.image }}" title="{{ user.nickname }}" width="56px" height="56xp" data-lightbox="group"/>
                  </a>
                </label>
              </td>
            </tr>
            {/* <tr><td className="td-color">ユーザー名</td><td className="td-indent">{{ user.username }}</td></tr>
            <tr><td className="td-color">メールアドレス</td><td className="td-indent">{{ user.email }}</td></tr>
            <tr><td className="td-color">投稿者名</td><td className="td-indent">{{ user.nickname }}</td></tr>
            <tr><td className="td-color">名前</td><td className="td-indent">{{ user.fullname }}</td></tr>
            <tr><td className="td-color">生年月日</td><td className="td-indent">{{ user.year }}年{{ user.month }}月{{ user.day }}日</td></tr>
            <tr><td className="td-color">年齢</td><td className="td-indent">{{ user.age }}歳</td></tr>
            <tr><td className="td-color">性別</td><td className="td-indent">{{ user.profile.get_gender_display }}</td></tr>
            <tr><td className="td-color">電話番号</td><td className="td-indent">{{ user.profile.phone }}</td></tr>
            <tr><td className="td-color">郵便番号</td><td className="td-indent">{{ user.profile.postal_code }}</td></tr>
            <tr><td className="td-color">住所</td><td className="td-indent">{{ user.prefecture }}{{ user.city }}{{ user.address }}{{ user.building }}</td></tr>
            <tr><td className="td-color">自己紹介</td><td className="td-indent">{{ user.profile.introduction|linebreaksbr|urlize }}</td></tr> */}
          </tbody>
        </table>

        <Footer/>
        {/* {% else %}
        <h2 className="login_required">ログインしてください</h2>
        {% endif %} */}
      </article>
    </>
  )
}
