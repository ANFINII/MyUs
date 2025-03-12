import { useRouter } from 'next/router'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import LoginError from 'components/parts/Error/Login'
import Input from 'components/parts/Input'
import Vertical from 'components/parts/Stack/Vertical'

export default function Withdrawal(): JSX.Element {
  const router = useRouter()
  const handleBack = () => router.push('/')
  const handleWithdrawal = () => router.push('/setting/withdrawal/confirm')

  const messages = false
  const message = '退会URL'
  const tokenSigned = false
  const expiredSeconds = 60

  return (
    <Main title="退会処理">
      <LoginError margin="mt_24">
        <article className="article_pass">
          <form method="POST" action="" className="form_account">
            {messages && (
              <ul className="messages_password_change">
                <li>{messages}</li>
              </ul>
            )}

            <Vertical gap="12">
              <p>{expiredSeconds}秒有効なURLを生成します</p>
              <Input type="password" name="password" placeholder="パスワード" minLength={8} maxLength={16} required />
            </Vertical>

            <Vertical gap="12" className='mv_40'>
              <Button color="green" size="l" name="退会URL生成" />
              {tokenSigned && <Button color="red" size="l" name="退会する" onClick={handleWithdrawal} />}
              {message && <Button color="red" size="l" name={message} />}
              <Button color="blue" size="l" name="ホーム" onClick={handleBack} />
            </Vertical>
          </form>
        </article>
      </LoginError>
      <Footer />
    </Main>
  )
}
