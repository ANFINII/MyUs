import Router from 'next/router'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import LoginRequired from 'components/parts/LoginRequired'

export default function WithdrawalConfirm() {
  const isAuthenticated = true

  return (
    <Main title="退会処理">
      <article className="article_pass">
        <LoginRequired isAuth>
          <form method="POST" action="" className="form_account">
            {/* <form method="POST" action="{% url 'myus:withdrawal' %}" className="form_account"> */}
            <p className="red mb_24">本当に退会しますか？</p>

            <Input type="password" name="password2" placeholder="パスワード" minLength={8} maxLength={16} className="mb_16" required />

            <Button red size="xl" name="退会する" className="w_full mv_24" />

            <Button blue size="xl" name="戻る" className="w_full mb_24" onClick={() => Router.push('/setting/withdrawal')} />
          </form>

          <Footer />
        </LoginRequired>
      </article>
    </Main>
  )
}
