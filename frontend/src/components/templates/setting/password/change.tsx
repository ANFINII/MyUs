import { ChangeEvent, useState } from 'react'
import { useRouter } from 'next/router'
import { useRequired } from 'components/hooks/useRequired'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import VStack from 'components/parts/Stack/Vertical'
import style from '../Setting.module.scss'

interface Values {
  oldPassword: string
  newPassword1: string
  newPassword2: string
}

export default function PasswordChange(): React.JSX.Element {
  const router = useRouter()
  const { isRequired, isRequiredCheck } = useRequired()
  const [values, setValues] = useState<Values>({ oldPassword: '', newPassword1: '', newPassword2: '' })

  const handleBack = () => router.push('/setting/profile')
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })

  const handleSubmit = () => {
    const { oldPassword, newPassword1, newPassword2 } = values
    if (!isRequiredCheck({ oldPassword, newPassword1, newPassword2 })) return
  }

  return (
    <Main title="パスワード変更">
      <article className={style.article_pass}>
        <form method="POST" action="" className={style.form_account}>
          <VStack gap="8">
            <Input
              type="password"
              name="oldPassword"
              minLength={8}
              maxLength={16}
              placeholder="現在パスワード"
              value={values.oldPassword}
              required={isRequired}
              onChange={handleInput}
            />
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
            <Button color="green" size="l" name="変更する" onClick={handleSubmit} />
            <Button color="blue" size="l" name="戻る" onClick={handleBack} />
          </VStack>
        </form>
      </article>
      <Footer />
    </Main>
  )
}
