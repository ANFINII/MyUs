import Router from 'next/router'
import Main from 'components/layouts/Main'
import Footer from 'components/layouts/Footer'
import Input from 'components/parts/Input'
import Button from 'components/parts/Button'

export default function Withdrawal() {
  const isAuthenticated = true
  const messages = false
  const message = '退会URL'
  const token_signed = false
  const expired_seconds = 60

  return (
    <Main title="MyUs退会処理" hero="退会処理">
      <article className="article_pass">
        {isAuthenticated ?
          <form method="POST" action="" className="form_account">
          {/* <form method="POST" action="{% url 'myus:withdrawal' %}" className="form_account"> */}
            {/* {% csrf_token %} */}
            {messages &&
              <ul className="messages_password_change">
              {/* {% for message in messages %}
              <li {% if message.tags %} className="{{ message.tags }}" {% endif %}>{{ message }}</li>
              {% endfor %} */}
              </ul>
            }

            <p className="bottom_24">{expired_seconds}秒有効なURLを生成します</p>

            <Input type="password" name="password" placeholder="パスワード" minLength={8} maxLength={16} className="bottom_16" required />

            <Button green size="xl" className="full vertical_24">退会URL生成</Button>

            {token_signed &&
              <Button red size="xl" onClick={() => Router.push('/setting/withdrawal/confirm')} className="full bottom_24">退会する</Button>
            }
            {message && <Button red size="xl" className="full bottom_24">{message}</Button>}

            <Button blue size="xl" onClick={() => Router.push('/')} className="full bottom_24">ホーム</Button>
          </form>
        :
          <h2 className="login_required">ログインしてください</h2>
        }
        <Footer />
      </article>
    </Main>
  )
}