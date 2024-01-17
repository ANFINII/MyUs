import { useState } from 'react'
import Head from 'next/head'
import Link from 'next/link'
import Router from 'next/router'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'

export default function LoginPage() {
  const [clicked, setClicked] = useState(false)

  const loginClicked = () => setClicked(!clicked)

  return (
    <Main>
      <article className="article_registration">
        <Head>
          <title>MyUsログイン</title>
        </Head>

        <form method="POST" action="" className="form_account">
          <h1 className="login_h1">MyUsへようこそ</h1>

          {/* {% if messages %}
          <ul className="messages_login">
            {% for message in messages %}
            <li {% if message.tags %} className="{{ message.tags }}" {% endif %}>{{ message }}</li>
            {% endfor %}
          </ul>
          {% endif %} */}

          <Input type="text" name="username" placeholder="ユーザー名 or メールアドレス" className="mb_16" required autoFocus />
          <Input type="password" name="password" placeholder="パスワード" minLength={8} maxLength={16} className="mb_16" required />

          <div className="password_reset">
            <Link href="/setting/password_reset">パスワードをリセット</Link>
          </div>

          <Button blue size="xl" type="submit" name="ログイン" className="full_w mb_24" onClick={loginClicked} />
          <Button green size="xl" name="アカウント登録" className="full_w mb_24" onClick={() => Router.push('/registration/signup')} />
        </form>

        <Footer />
      </article>
    </Main>
  )
}
