import { ChangeEvent, useState } from 'react'
import { useRouter } from 'next/router'
import { WithdrawalIn } from 'types/internal/auth'
import { postWithdrawal } from 'api/internal/auth'
import { FetchError } from 'utils/constants/enum'
import { encrypt } from 'utils/functions/encrypt'
import { useIsLoading } from 'components/hooks/useIsLoading'
import { useRequired } from 'components/hooks/useRequired'
import { useToast } from 'components/hooks/useToast'
import { useUser } from 'components/hooks/useUser'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import VStack from 'components/parts/Stack/Vertical'
import style from '../Setting.module.scss'

export default function WithdrawalConfirm(): React.JSX.Element {
  const router = useRouter()
  const { resetUser } = useUser()
  const { isLoading, handleLoading } = useIsLoading()
  const { isRequired, isRequiredCheck } = useRequired()
  const { toast, handleToast } = useToast()
  const [values, setValues] = useState<WithdrawalIn>({ password: '' })

  const handleBack = () => router.push('/setting/withdrawal')
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })

  const handleSubmit = async () => {
    const { password } = values
    if (!isRequiredCheck({ password })) return

    handleLoading(true)
    const request: WithdrawalIn = { password: encrypt(password) }
    const ret = await postWithdrawal(request)
    handleLoading(false)
    if (ret.isErr()) {
      handleToast(FetchError.Post, true)
      return
    }
    resetUser()
    router.push('/account/login')
  }

  return (
    <Main title="退会処理" toast={toast}>
      <article className={style.article_pass}>
        <form method="POST" action="" className={style.form_account}>
          <VStack gap="8">
            <p className="red">本当に退会しますか？</p>
            <Input
              type="password"
              name="password"
              minLength={8}
              maxLength={16}
              placeholder="パスワード"
              value={values.password}
              required={isRequired}
              onChange={handleInput}
            />
          </VStack>

          <VStack gap="12" className="mv_40">
            <Button color="red" size="l" name="退会する" loading={isLoading} onClick={handleSubmit} />
            <Button color="blue" size="l" name="戻る" onClick={handleBack} />
          </VStack>
        </form>
      </article>
      <Footer />
    </Main>
  )
}
