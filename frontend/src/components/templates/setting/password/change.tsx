import { ChangeEvent, useState } from 'react'
import { useRouter } from 'next/router'
import { PasswordChangeIn } from 'types/internal/auth'
import { postPasswordChange } from 'api/internal/auth'
import { FetchError } from 'utils/constants/enum'
import { encrypt } from 'utils/functions/encrypt'
import { useLoading } from 'components/hooks/useLoading'
import { useRequired } from 'components/hooks/useRequired'
import { useToast } from 'components/hooks/useToast'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import VStack from 'components/parts/Stack/Vertical'
import Password from 'components/widgets/Password'
import style from '../Setting.module.scss'

export default function PasswordChange(): React.JSX.Element {
  const router = useRouter()
  const { loading, handleLoading } = useLoading()
  const { error, validate } = useRequired()
  const { toast, handleToast } = useToast()
  const [values, setValues] = useState<PasswordChangeIn>({ oldPassword: '', password1: '', password2: '' })

  const handleBack = () => router.push('/setting/profile')
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })

  const handleSubmit = async () => {
    const { oldPassword, password1, password2 } = values
    if (!validate({ oldPassword, password1, password2 })) return
    if (password1 !== password2) {
      handleToast('新規パスワードが一致しません', true)
      return
    }
    handleLoading(true)
    const request: PasswordChangeIn = {
      oldPassword: encrypt(oldPassword),
      password1: encrypt(password1),
      password2: encrypt(password2),
    }
    const ret = await postPasswordChange(request)
    handleLoading(false)
    if (ret.isErr()) {
      handleToast(FetchError.Post, true)
      return
    }
    router.push('/setting/password/change-done')
  }

  return (
    <Main title="パスワード変更" toast={toast}>
      <article className={style.article_pass}>
        <form method="POST" action="" className={style.form_account}>
          <VStack gap="8">
            <Password value={values.oldPassword} name="oldPassword" placeholder="現在パスワード" error={error} onChange={handleInput} />
            <Password value={values.password1} name="password1" placeholder="パスワード(英数字8~16文字)" error={error} onChange={handleInput} />
            <Password value={values.password2} name="password2" placeholder="パスワード(確認用)" error={error} onChange={handleInput} />
          </VStack>

          <VStack gap="12" className="mv_40">
            <Button color="green" size="l" name="変更する" loading={loading} onClick={handleSubmit} />
            <Button color="blue" size="l" name="戻る" onClick={handleBack} />
          </VStack>
        </form>
      </article>
      <Footer />
    </Main>
  )
}
