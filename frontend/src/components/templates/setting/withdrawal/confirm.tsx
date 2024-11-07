import { useRouter } from 'next/router'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import LoginRequired from 'components/parts/LoginRequired'

export default function WithdrawalConfirm() {
  const router = useRouter()

  return (
    <Main title="退会処理">
      <LoginRequired>
        <article className="article_pass">
          <form method="POST" action="" className="form_account">
            {/* <form method="POST" action="{% url 'app:withdrawal' %}" className="form_account"> */}
            <p className="red mb_24">本当に退会しますか？</p>

            <Input type="password" name="password2" placeholder="パスワード" minLength={8} maxLength={16} className="mb_16" required />

            <Button color="red" size="l" name="退会する" className="w_full mv_24" />

            <Button color="blue" size="l" name="戻る" className="w_full mb_24" onClick={() => router.push('/setting/withdrawal')} />
          </form>

          <Footer />
        </article>
      </LoginRequired>
    </Main>
  )
}
