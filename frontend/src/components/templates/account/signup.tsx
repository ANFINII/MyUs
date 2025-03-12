import { useState, ChangeEvent } from 'react'
import { useRouter } from 'next/router'
import { SignupIn } from 'types/internal/auth'
import { postSignup } from 'api/internal/auth'
import { Gender } from 'utils/constants/enum'
import { nowDate, selectDate } from 'utils/functions/datetime'
import { genders } from 'utils/functions/user'
import { useToast } from 'components/hooks/useToast'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import Radio from 'components/parts/Input/Radio'
import Select from 'components/parts/Input/Select'
import Horizontal from 'components/parts/Stack/Horizontal'
import Vertical from 'components/parts/Stack/Vertical'

const initSignup: SignupIn = {
  email: '',
  username: '',
  nickname: '',
  password1: '',
  password2: '',
  fullName: '',
  lastName: '',
  firstName: '',
  year: nowDate.year - 50,
  month: 6,
  day: 15,
  gender: Gender.Male,
}

export default function Signup(): JSX.Element {
  const router = useRouter()
  const { toast, handleToast } = useToast()
  const [message, setMessage] = useState<string>('')
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [isRequired, setIsRequired] = useState<boolean>(false)
  const [values, setValues] = useState<SignupIn>(initSignup)

  const { years, months, days } = selectDate()
  const handleBack = () => router.push('/account/login')
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleSelect = (e: ChangeEvent<HTMLSelectElement>) => setValues({ ...values, [e.target.name]: e.target.value })

  const handleSubmit = async () => {
    const { email, username, nickname, lastName, firstName, password1, password2 } = values
    if (!(email && username && nickname && lastName && firstName && password1 && password2)) {
      setIsRequired(true)
      return
    }
    setIsLoading(true)
    try {
      const data = await postSignup(values)
      if (data) setMessage(data.message)
      if (!data?.error) handleBack()
    } catch {
      handleToast('エラーが発生しました！', true)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Main metaTitle="アカウント登録" toast={toast}>
      <article className="article_registration">
        <form method="POST" action="" className="form_account">
          <h1 className="signup_h1">アカウント登録</h1>

          {message && (
            <ul className="messages_signup">
              <li>{message}</li>
            </ul>
          )}

          <Vertical gap="8">
            <Vertical gap="4">
              <p>名前</p>
              <div className="name_group">
                <Input name="lastName" placeholder="姓" maxLength={30} required={isRequired} onChange={handleInput} />
                <Input name="firstName" placeholder="名" maxLength={30} required={isRequired} onChange={handleInput} />
              </div>
            </Vertical>

            <Input name="username" placeholder="ユーザー名(英数字)" maxLength={20} required={isRequired} onChange={handleInput} />
            <Input name="nickname" placeholder="投稿者名" maxLength={80} required={isRequired} onChange={handleInput} />
            <Input type="email" name="email" placeholder="メールアドレス" maxLength={255} required={isRequired} onChange={handleInput} />
            <Input type="password" name="password1" placeholder="パスワード(英数字8~16文字)" minLength={8} maxLength={16} required={isRequired} onChange={handleInput} />
            <Input type="password" name="password2" placeholder="パスワード(確認用)" minLength={8} maxLength={16} required={isRequired} onChange={handleInput} />

            <Vertical gap="4">
              <p>生年月日</p>
              <Horizontal gap="2" full>
                <Select name="year" value={values.year} options={years} onChange={handleSelect} />
                <Select name="month" value={values.month} options={months} onChange={handleSelect} />
                <Select name="day" value={values.day} options={days} onChange={handleSelect} />
              </Horizontal>
            </Vertical>

            <Vertical gap="4">
              <p>性別</p>
              <Horizontal gap="5">
                {genders.map((gender) => (
                  <Radio key={gender.key} label={gender.key} name="gender" value={gender.value} checked={gender.value === values.gender} onChange={handleInput} />
                ))}
              </Horizontal>
            </Vertical>
          </Vertical>

          <Vertical gap="12" className='mv_40'>
            <Button color="green" size="l" name="アカウント登録" type="submit" loading={isLoading} onClick={handleSubmit} />
            <Button color="blue" size="l" name="戻る" onClick={handleBack} />
          </Vertical>
        </form>
      </article>
      <Footer />
    </Main>
  )
}
