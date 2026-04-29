import { ChangeEvent, useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import { PasswordResetIn } from 'types/internal/auth'
import { getPasswordResetVerify, postPasswordReset } from 'api/internal/auth'
import { FetchError } from 'utils/constants/enum'
import { encrypt } from 'utils/functions/encrypt'
import { useIsLoading } from 'components/hooks/useIsLoading'
import { useRequired } from 'components/hooks/useRequired'
import { useToast } from 'components/hooks/useToast'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import VStack from 'components/parts/Stack/Vertical'

export default function ResetConfirm(): React.JSX.Element {
  const router = useRouter()
  const { isLoading, handleLoading } = useIsLoading()
  const { isRequired, isRequiredCheck } = useRequired()
  const { toast, handleToast } = useToast()
  const [email, setEmail] = useState<string>('')
  const [isVerified, setIsVerified] = useState<boolean>(false)
  const [values, setValues] = useState<PasswordResetIn>({ token: '', newPassword1: '', newPassword2: '' })

  const handleBack = () => router.push('/account/login')
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })

  useEffect(() => {
    if (!router.isReady) return
    const token = router.query.token
    if (typeof token !== 'string' || token === '') {
      router.push('/account/login')
      return
    }
    const verify = async () => {
      const ret = await getPasswordResetVerify(token)
      if (ret.isErr()) {
        router.push('/account/login')
        return
      }
      setValues((prev) => ({ ...prev, token }))
      setEmail(ret.value.email)
      setIsVerified(true)
    }
    verify()
  }, [router])

  const handleSubmit = async () => {
    const { newPassword1, newPassword2 } = values
    if (!isRequiredCheck({ newPassword1, newPassword2 })) return
    if (newPassword1 !== newPassword2) {
      handleToast('新規パスワードが一致しません', true)
      return
    }
    handleLoading(true)
    const request: PasswordResetIn = {
      token: values.token,
      newPassword1: encrypt(newPassword1),
      newPassword2: encrypt(newPassword2),
    }
    const ret = await postPasswordReset(request)
    handleLoading(false)
    if (ret.isErr()) {
      handleToast(ret.error.message ?? FetchError.Post, true)
      return
    }
    router.push('/account/reset/done')
  }

  return (
    <Main metaTitle="パスワード再設定" toast={toast}>
      <article className="article_registration">
        <form method="POST" action="" className="form_account">
          <h1 className="login_h1">パスワード再設定</h1>

          {isVerified && (
            <>
              <VStack gap="8">
                <Input type="email" name="email" value={email} disabled maxLength={255} />
                <Input
                  type="password"
                  name="newPassword1"
                  minLength={8}
                  maxLength={16}
                  placeholder="新規パスワード(英数字8~16文字)"
                  value={values.newPassword1}
                  required={isRequired}
                  onChange={handleInput}
                />
                <Input
                  type="password"
                  name="newPassword2"
                  minLength={8}
                  maxLength={16}
                  placeholder="新規パスワード(確認用)"
                  value={values.newPassword2}
                  required={isRequired}
                  onChange={handleInput}
                />
              </VStack>

              <VStack gap="12" className="mv_40">
                <Button color="green" size="l" name="再設定" type="submit" loading={isLoading} onClick={handleSubmit} />
                <Button color="blue" size="l" name="戻る" onClick={handleBack} />
              </VStack>
            </>
          )}
        </form>
      </article>
      <Footer />
    </Main>
  )
}
