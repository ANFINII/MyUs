import { useState, ChangeEvent } from 'react'
import { useRouter } from 'next/router'
import { postReset } from 'api/internal/auth'
import { FetchError } from 'utils/constants/enum'
import { useRequired } from 'components/hooks/useRequired'
import { useToast } from 'components/hooks/useToast'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import Vertical from 'components/parts/Stack/Vertical'

export default function Reset(): JSX.Element {
  const router = useRouter()
  const { toast, handleToast } = useToast()
  const { isRequired, isRequiredCheck } = useRequired()
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [message, setMessage] = useState<string>('')
  const [email, setEmail] = useState<string>('')

  const handleBack = () => router.push('/account/login')
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setEmail(e.target.value)

  const handleSubmit = async () => {
    if (!isRequiredCheck({ email })) return
    setIsLoading(true)
    const ret = await postReset(email)
    if (ret.isErr()) return handleToast(FetchError.Error, true)
    const data = ret.value
    if (data) setMessage(data.message)
    setIsLoading(false)
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

          <Input type="email" placeholder="メールアドレス" required={isRequired} onChange={handleInput} />

          <Vertical gap="12" className="mv_40">
            <Button color="green" size="l" name="送信" type="submit" loading={isLoading} onClick={handleSubmit} />
            <Button color="blue" size="l" name="戻る" onClick={handleBack} />
          </Vertical>
        </form>
      </article>
      <Footer />
    </Main>
  )
}
