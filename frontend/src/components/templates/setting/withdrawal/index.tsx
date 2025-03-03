import { useRouter } from 'next/router'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import LoginError from 'components/parts/Error/Login'
import Input from 'components/parts/Input'

export default function Withdrawal(): JSX.Element {
  const router = useRouter()

  const messages = false
  const message = '退会URL'
  const tokenSigned = false
  const expiredSeconds = 60

  return (
    <Main title="退会処理">
      <LoginError margin="mt_24">
        <article className="article_pass">
          <form method="POST" action="" className="form_account">
            {/* <form method="POST" action="{% url 'app:withdrawal' %}" className="form_account"> */}
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

            {tokenSigned && <Button color="red" size="l" name="退会する" className="w_full mb_24" onClick={() => router.push('/setting/withdrawal/confirm')} />}
            {message && <Button color="red" size="l" name={message} className="w_full mb_24" />}

            <Button color="blue" size="l" name="ホーム" className="w_full mb_24" onClick={() => router.push('/')} />
          </form>
          <Footer />
        </article>
      </LoginError>
    </Main>
  )
}
