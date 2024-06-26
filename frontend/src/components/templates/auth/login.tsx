import { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/router'
import { postLogin } from 'api/auth'
import { LoginIn } from 'types/internal/auth'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'

export default function Login() {
  const router = useRouter()
  const [message, setMessage] = useState<string>('')
  const [isRequired, setIsRequired] = useState<boolean>(false)
  const [data, setData] = useState<LoginIn>({ username: '', password: '' })

  const handleUsername = (username: string) => setData({ ...data, username })
  const handlePassword = (password: string) => setData({ ...data, password })

  const handleSubmit = async () => {
    if (!(data.username && data.password)) {
      setIsRequired(true)
      return
    }
    try {
      const resData = await postLogin(data)
      if (resData?.message) {
        setMessage(resData.message)
      } else {
        localStorage.removeItem('user')
        localStorage.setItem('user', JSON.stringify(resData.user))
        router.push('/setting/profile')
      }
    } catch (e) {
      setMessage('エラーが発生しました！')
    }
  }

  return (
    <Main title="ログイン">
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

          <div className="password_reset">
            <Link href="/setting/password_reset">パスワードをリセット</Link>
          </div>

          <Button color="blue" size="l" name="ログイン" className="w_full mb_24" onClick={handleSubmit} />
          <Button color="green" size="l" name="アカウント登録" className="w_full mb_24" onClick={() => router.push('/registration/signup')} />
        </form>
        <Footer />
      </article>
      <Footer />
    </Main>
  )
}
