import Router from 'next/router'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'

export default function Withdrawal() {
  const isAuthenticated = true
  const messages = false
  const message = '退会URL'
  const tokenSigned = false
  const expiredSeconds = 60

  return (
    <Main title="退会処理">
      <article className="article_pass">
        {isAuthenticated ? (
          <form method="POST" action="" className="form_account">
            {/* <form method="POST" action="{% url 'myus:withdrawal' %}" className="form_account"> */}
            {/* {% csrf_token %} */}
            {messages && (
              <ul className="messages_password_change">
                {/* {% for message in messages %}
              <li {% if message.tags %} className="{{ message.tags }}" {% endif %}>{{ message }}</li>
              {% endfor %} */}
              </ul>
            )}

            <p className="mb_24">{expiredSeconds}秒有効なURLを生成します</p>

            <Input type="password" name="password" placeholder="パスワード" minLength={8} maxLength={16} className="mb_16" required />

            <Button green size="xl" name="退会URL生成" className="full_w mv_24" />

            {tokenSigned && <Button red size="xl" name="退会する" className="full_w mb_24" onClick={() => Router.push('/setting/withdrawal/confirm')} />}
            {message && <Button red size="xl" name={message} className="full_w mb_24" />}

            <Button blue size="xl" name="ホーム" className="full_w mb_24" onClick={() => Router.push('/')} />
          </form>
        ) : (
          <h2 className="login_required">ログインしてください</h2>
        )}
        <Footer />
      </article>
    </Main>
  )
}
