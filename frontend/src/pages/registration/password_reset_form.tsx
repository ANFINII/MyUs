import Head from 'next/head'
import Link from 'next/link'
import Footer from 'components/layout/Footer'


export default function PasswordResetForm() {
  return (
    <article className="article_registration">
      <Head>
        <title>MyUsパスワードリセット</title>
      </Head>

      <form method="POST" action="" className="form_account">
        {/* {% csrf_token %} */}
        <h1 className="myus_h1">パスワードをリセット</h1>
        {/* {% if errors %} */}
        {/* <p className="messages_password_form">{{ form.email.errors }}</p> */}
        {/* {% endif %} */}

        <p><input type="email" name="email" placeholder="メールアドレス" className="form-control email_reset" autoComplete="email" required autoFocus/></p>

        <p><input type="submit" value="送信" id="submit" className="btn btn-lg btn-success btn-block"/></p>

        <p>
          <Link href="/login" className="btn btn-lg btn-primary btn-block">戻る</Link>
        </p>
      </form>
      <Footer />
    </article>
  )
}
