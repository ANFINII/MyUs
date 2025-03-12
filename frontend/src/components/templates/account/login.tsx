import { useState, ChangeEvent } from 'react'
import { useRouter } from 'next/router'
import { LoginIn } from 'types/internal/auth'
import { postLogin } from 'api/internal/auth'
import { useToast } from 'components/hooks/useToast'
import { useUser } from 'components/hooks/useUser'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import Vertical from 'components/parts/Stack/Vertical'

export default function Login(): JSX.Element {
  const router = useRouter()
  const { updateUser } = useUser()
  const { toast, handleToast } = useToast()
  const [message, setMessage] = useState<string>('')
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [isRequired, setIsRequired] = useState<boolean>(false)
  const [values, setValues] = useState<LoginIn>({ username: '', password: '' })

  const handleSignup = () => router.push('/account/signup')
  const handleReset = () => router.push('/account/reset')
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })

  const handleSubmit = async () => {
    if (!(values.username && values.password)) {
      setIsRequired(true)
      return
    }
    setIsLoading(true)
    try {
      const data = await postLogin(values)
      if (data) setMessage(data.message)
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

          <Vertical gap="8">
            <Input type="text" name="username" placeholder="ユーザー名 or メールアドレス" required={isRequired} onChange={handleInput} />
            <Input type="password" name="password" placeholder="パスワード" minLength={8} maxLength={16} required={isRequired} onChange={handleInput} />
            <p className="password_reset" onClick={handleReset}>パスワードをリセット</p>
          </Vertical>

          <div className='mv_40'>
            <Vertical gap="12">
              <Button color="blue" size="l" name="ログイン" type="submit" loading={isLoading} onClick={handleSubmit} />
              <Button color="green" size="l" name="アカウント登録" onClick={handleSignup} />
            </Vertical>
          </div>
        </form>
      </article>
      <Footer />
    </Main>
  )
}
