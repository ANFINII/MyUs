import { useRouter } from 'next/router'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import LoginError from 'components/parts/Error/Login'
import Input from 'components/parts/Input'

export default function WithdrawalConfirm(): JSX.Element {
  const router = useRouter()

  return (
    <Main title="退会処理">
      <LoginError>
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
      </LoginError>
    </Main>
  )
}
