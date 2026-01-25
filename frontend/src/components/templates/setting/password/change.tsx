import { useRouter } from 'next/router'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import VStack from 'components/parts/Stack/Vertical'

export default function PasswordChange(): React.JSX.Element {
  const router = useRouter()
  const handleBack = () => router.push('/setting/profile')

  return (
    <Main title="パスワード変更">
      <article className="article_pass">
        <form method="POST" action="" className="form_account">
          <ul className="messages_password_change">
            <li>{/* { form.old_password.errors } */}</li>
            <li>{/* { form.new_password2.errors } */}</li>
          </ul>

          <VStack gap="8">
            <Input type="password" name="old_password" minLength={8} maxLength={16} placeholder="現在パスワード" required />
            <Input type="password" name="new_password1" minLength={8} maxLength={16} placeholder="新規パスワード(英数字8~16文字)" required />
            <Input type="password" name="new_password2" minLength={8} maxLength={16} placeholder="新規パスワード(確認用)" required />
          </VStack>

          <VStack gap="12" className="mv_40">
            <Button color="red" size="l" name="退会する" />
            <Button color="blue" size="l" name="戻る" onClick={handleBack} />
          </VStack>
        </form>
      </article>
      <Footer />
    </Main>
  )
}
