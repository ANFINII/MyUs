import { useState } from 'react'
import { useRouter } from 'next/router'
import { LoginIn } from 'types/internal/auth'
import { postLogin } from 'api/internal/auth'
import { useToast } from 'components/hooks/useToast'
import { useUser } from 'components/hooks/useUser'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'

export default function Login() {
  const router = useRouter()
  const { updateUser } = useUser()
  const { toast, handleToast } = useToast()
  const [message, setMessage] = useState<string>('')
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [isRequired, setIsRequired] = useState<boolean>(false)
  const [values, setValues] = useState<LoginIn>({ username: '', password: '' })

  const handleSignup = () => router.push('/account/signup')
  const handleReset = () => router.push('/account/reset')
  const handleUsername = (username: string) => setValues({ ...values, username })
  const handlePassword = (password: string) => setValues({ ...values, password })

  const handleSubmit = async () => {
    if (!(values.username && values.password)) {
      setIsRequired(true)
      return
    }
    setIsLoading(true)
    try {
      const data = await postLogin(values)
      data && setMessage(data.message)
      if (!data?.error) {
        await updateUser()
        router.push('/setting/profile')
      }
    } catch {
      handleToast('エラーが発生しました！', true)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Main title="ログイン" toast={toast}>
      <article className="article_registration">
        <form method="POST" action="" className="form_account">
          <h1 className="login_h1">MyUsへようこそ</h1>

          {message && (
            <ul className="messages_login">
              <li>{message}</li>
            </ul>
          )}

          <Input type="text" placeholder="ユーザー名 or メールアドレス" className="mb_16" required={isRequired} autoFocus onChange={handleUsername} />
          <Input type="password" placeholder="パスワード" minLength={8} maxLength={16} className="mb_16" required={isRequired} onChange={handlePassword} />

          <p className="password_reset" onClick={handleReset}>
            パスワードをリセット
          </p>

          <Button color="blue" size="l" name="ログイン" type="submit" className="w_full mb_24" loading={isLoading} onClick={handleSubmit} />
          <Button color="green" size="l" name="アカウント登録" className="w_full mb_24" onClick={handleSignup} />
        </form>
        <Footer />
      </article>
      <Footer />
    </Main>
  )
}
