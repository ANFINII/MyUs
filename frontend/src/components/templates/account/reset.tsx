import { useState } from 'react'
import { useRouter } from 'next/router'
import { postReset } from 'api/internal/auth'
import { useToast } from 'components/hooks/useToast'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'

export default function Reset() {
  const router = useRouter()
  const { toast, handleToast } = useToast()
  const [message, setMessage] = useState<string>('')
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [isRequired, setIsRequired] = useState<boolean>(false)
  const [email, setEmail] = useState<string>('')

  const handleBack = () => router.push('/account/login')
  const handleEmail = (email: string) => setEmail(email)

  const handleSubmit = async () => {
    if (!email) {
      setIsRequired(true)
      return
    }
    setIsLoading(true)
    try {
      const data = await postReset(email)
      data && setMessage(data.message)
    } catch (e) {
      handleToast('エラーが発生しました！', true)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Main metaTitle="パスワードリセット" toast={toast}>
      <article className="article_registration">
        <form method="POST" action="" className="form_account">
          <h1 className="login_h1">パスワードリセット</h1>

          {message && (
            <ul className="messages_login">
              <li>{message}</li>
            </ul>
          )}

          <Input type="email" placeholder="メールアドレス" className="mb_40" required={isRequired} onChange={handleEmail} />
          <Button color="green" size="l" name="送信" type="submit" className="w_full mb_24" loading={isLoading} onClick={handleSubmit} />
          <Button color="blue" size="l" name="戻る" className="w_full mb_24" onClick={handleBack} />
        </form>
        <Footer />
      </article>
      <Footer />
    </Main>
  )
}
