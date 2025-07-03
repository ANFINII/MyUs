import { useRouter } from 'next/router'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import LoginError from 'components/parts/Error/Login'
import Input from 'components/parts/Input'
import VStack from 'components/parts/Stack/Vertical'

export default function WithdrawalConfirm(): JSX.Element {
  const router = useRouter()
  const handleBack = () => router.push('/setting/withdrawal')

  return (
    <Main title="退会処理">
      <LoginError>
        <article className="article_pass">
          <form method="POST" action="" className="form_account">
            <VStack gap="8">
              <p className="red">本当に退会しますか？</p>
              <Input type="password" name="password2" placeholder="パスワード" minLength={8} maxLength={16} required />
            </VStack>

            <VStack gap="12" className="mv_40">
              <Button color="red" size="l" name="退会する" />
              <Button color="blue" size="l" name="戻る" onClick={handleBack} />
            </VStack>
          </form>
        </article>
      </LoginError>
      <Footer />
    </Main>
  )
}
