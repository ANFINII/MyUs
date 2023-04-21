import Router from 'next/router'
import Main from 'components/layouts/Main'
import Footer from 'components/layouts/Footer'
import Input from 'components/parts/Input'
import Button from 'components/parts/Button'

export default function Withdrawal() {
  const isAuthenticated = true
  const messages = false
  const message = false
  const token_signed = false
  const expired_seconds = 60

  return (
    <Main title="MyUs退会処理" hero="退会処理">
      <article className="article_pass">
        {isAuthenticated ?
          <form method="POST" action="" className="form_signup">
          {/* <form method="POST" action="{% url 'myus:withdrawal' %}" className="form_signup"> */}
            {/* {% csrf_token %} */}
            {messages &&
              <ul className="messages_password_change">
              {/* {% for message in messages %}
              <li {% if message.tags %} className="{{ message.tags }}" {% endif %}>{{ message }}</li>
              {% endfor %} */}
              </ul>
            }

            <p>{expired_seconds}秒有効なURLを生成します</p>
            <br />

            <Input type="password" name="password" placeholder="パスワード" minLength={8} maxLength={16} className="input_margin" required />

            <Button green size="xl" className="button_margin">退会URL生成</Button>

            <p className="withdrawal">
            {token_signed &&
              <Button red size="xl" onClick={() => Router.push('/setting/withdrawal/confirm')} className="button_margin">退会する</Button>
            }
            {message && <button className="button red xl button_margin">{message}</button>}
            </p>

            <Button blue size="xl" onClick={() => Router.push('/')} className="button_margin">ホーム</Button>
          </form>
        :
          <h2 className="login_required">ログインしてください</h2>
        }
        <Footer />
      </article>
    </Main>
  )
}
