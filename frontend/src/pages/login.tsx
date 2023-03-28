import Head from 'next/head'
import Link from 'next/link'
import Router from 'next/router'
import {useState} from 'react'
import Footer from 'components/layouts/Footer'
import Input from 'components/parts/Input'
import Button from 'components/parts/Button'

export default function Login() {
  const url = process.env.NEXT_PUBLIC_API_URL
  const token = process.env.TOKEN
  // const [token, setToken] = useState([])
  const [clicked, setClicked] = useState(false)

  const loginClicked = () => {
    setClicked(!clicked)
  }

  return (
    <article className="article_registration">
      <Head>
        <title>MyUsログイン</title>
      </Head>

      <form method="POST" action="" className="form_signup">
        {/* {% csrf_token %} */}
        <h1 className="login_h1">MyUsへようこそ</h1>

        {/* {% if messages %}
        <ul className="messages_login">
          {% for message in messages %}
          <li {% if message.tags %} className="{{ message.tags }}" {% endif %}>{{ message }}</li>
          {% endfor %}
        </ul>
        {% endif %} */}

        <Input type="username" name="username" className="inpput_margin" placeholder="ユーザー名 or メールアドレス" required autoFocus />
        <Input type="password" name="password" className="inpput_margin" placeholder="パスワード" minLength={8} maxLength={16} required />

        <div className="password_reset">
          <Link href="/setting/password_reset">パスワードをリセット</Link>
        </div>

        <Button blue size="xl" type="submit" onClick={loginClicked} className="button_margin">ログイン</Button>
        <Button green size="xl" className="button_margin" onClick={() => Router.push('/registration/signup')}>アカウント登録</Button>
      </form>

      <Footer />
    </article>
  )
}
