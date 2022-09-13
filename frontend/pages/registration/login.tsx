import Head from 'next/head'
import Link from 'next/link'
import Footer from 'components/layouts/footer'

export default function Login() {
  return (
    <>
      <Head>
        <title>MyUsログイン</title>
      </Head>

      <form method="POST" action="" className="form-signup">
        {/* {% csrf_token %} */}
        <h1 className="myus_h1">MyUsへようこそ</h1>

        {/* {% if messages %}
        <ul className="messages_login">
          {% for message in messages %}
          <li {% if message.tags %} className="{{ message.tags }}" {% endif %}>{{ message }}</li>
          {% endfor %}
        </ul>
        {% endif %} */}

        <p><input type="username" name="username" id="username" className="form-control" placeholder="ユーザー名 or メールアドレス" required autoFocus/></p>

        <p><input type="password" name="password" id="password" className="form-control" placeholder="パスワード" minLength={8} maxLength={16} required/></p>

        <div className="password_reset">
          <Link href="/registration/password_reset" as="/password_reset">
            <a href="{% url 'password_reset' %}">パスワードをリセット</a>
          </Link>
        </div>

        <p><input type="submit" value="ログイン" id="login" className="btn btn-lg btn-primary btn-block"/></p>

        <Link href="/registration/signup" as="/signup">
          <a className="btn btn-lg btn-success btn-block" role="button">アカウント登録</a>
        </Link>
      </form>
      <Footer/>
    </>
  )
}
