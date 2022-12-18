import Head from 'next/head'
import Link from 'next/link'
import Footer from 'components/layouts/footer'
// import axios from 'pages/api/axios'
import { useRouter } from "next/router"
import { useState } from 'react'


export default function Login() {
  const router = useRouter();
  const url = process.env.NEXT_PUBLIC_API_URL
  const token = process.env.TOKEN
  // const [token, setToken] = useState([])
  const [clicked, setClicked] = useState(false)

  const loginClicked = () => {
    setClicked(!clicked)
  }

  // axios.post(url + '/api/login', {
  //   headers: {
  //     'Content-Type': 'application/json'
  // }
  // })
  // .then(res => {
  //   console.log(res.data)
  // })
  // .catch(e => {
  //   console.log(e)
  // })

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

        <p><input type="username" name="username" id="username" className="form-control" placeholder="ユーザー名 or メールアドレス" required autoFocus/></p>

        <p><input type="password" name="password" id="password" className="form-control" placeholder="パスワード" minLength={8} maxLength={16} required/></p>

        <div className="password_reset">
          <Link href="/registration/password_reset">パスワードをリセット</Link>
        </div>

        <p><button type="button" id="login" onClick={loginClicked} className="btn btn-lg btn-primary btn-block">ログイン</button></p>

        <Link href="/registration/signup" className="btn btn-lg btn-success btn-block">アカウント登録</Link>
      </form>

      <Footer/>
    </article>
  )
}
