import Router from 'next/router'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import LoginRequired from 'components/parts/LoginRequired'

export default function Withdrawal() {
  const isAuthenticated = true
  const messages = false
  const message = '退会URL'
  const tokenSigned = false
  const expiredSeconds = 60

  return (
    <Main title="退会処理">
      <article className="article_pass">
        <LoginRequired isAuth>
          <form method="POST" action="" className="form_account">
            {/* <form method="POST" action="{% url 'myus:withdrawal' %}" className="form_account"> */}
            {messages && (
              <ul className="messages_password_change">
                {/* {% for message in messages %}
              <li {% if message.tags %} className="{{ message.tags }}" {% endif %}>{{ message }}</li>
              {% endfor %} */}
              </ul>
            )}

            <p className="mb_24">{expiredSeconds}秒有効なURLを生成します</p>

            <Input type="password" name="password" placeholder="パスワード" minLength={8} maxLength={16} className="mb_16" required />

            <Button color="green" size="l" name="退会URL生成" className="w_full mv_24" />

            {tokenSigned && <Button color="red" size="l" name="退会する" className="w_full mb_24" onClick={() => Router.push('/setting/withdrawal/confirm')} />}
            {message && <Button color="red" size="l" name={message} className="w_full mb_24" />}

            <Button color="blue" size="l" name="ホーム" className="w_full mb_24" onClick={() => Router.push('/')} />
          </form>
          <Footer />
        </LoginRequired>
      </article>
    </Main>
  )
}
