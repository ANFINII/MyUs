import { ChangeEvent, useState } from 'react'
import { useRouter } from 'next/router'
import { postSignupEmail } from 'api/internal/auth'
import { FetchError } from 'utils/constants/enum'
import { useIsLoading } from 'components/hooks/useIsLoading'
import { useRequired } from 'components/hooks/useRequired'
import { useToast } from 'components/hooks/useToast'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Alert from 'components/parts/Alert'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import VStack from 'components/parts/Stack/Vertical'

export default function Signup(): React.JSX.Element {
  const router = useRouter()
  const { isLoading, handleLoading } = useIsLoading()
  const { isRequired, isRequiredCheck } = useRequired()
  const { toast, handleToast } = useToast()
  const [email, setEmail] = useState<string>('')

  const handleBack = () => router.push('/account/login')
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setEmail(e.target.value)

  const handleSubmit = async () => {
    if (!isRequiredCheck({ email })) return
    handleLoading(true)
    const ret = await postSignupEmail(email)
    handleLoading(false)
    if (ret.isErr()) {
      handleToast(FetchError.Error, true)
      return
    }
    handleToast('メールを送信しました!', false)
  }

  return (
    <Main metaTitle="アカウント登録" toast={toast}>
      <article className="article_registration">
        <form method="POST" action="" className="form_account">
          <h1 className="signup_h1">アカウント登録</h1>

          <VStack gap="8">
            <Input type="email" name="email" placeholder="メールアドレス" maxLength={255} required={isRequired} onChange={handleInput} />
            <Alert type="info">
              メールアドレス宛に本登録用リンクを送信します。
              <br />
              リンクの有効期限は12時間です。
            </Alert>
          </VStack>

          <VStack gap="12" className="mv_40">
            <Button color="green" size="l" name="送信" type="submit" loading={isLoading} onClick={handleSubmit} />
            <Button color="blue" size="l" name="戻る" onClick={handleBack} />
          </VStack>
        </form>
      </article>
      <Footer />
    </Main>
  )
}
