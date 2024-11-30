import { useState } from 'react'
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
import Select from 'components/parts/Input/Select'

const initSignup: SignupIn = {
  email: '',
  username: '',
  nickname: '',
  password1: '',
  password2: '',
  fullName: '',
  lastName: '',
  firstName: '',
  year: (nowDate.year + 1900) / 2,
  month: 6,
  day: 15,
  gender: Gender.Male,
}

export default function Signup() {
  const router = useRouter()
  const { toast, handleToast } = useToast()
  const [message, setMessage] = useState<string>('')
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [isRequired, setIsRequired] = useState<boolean>(false)
  const [values, setValues] = useState<SignupIn>(initSignup)

  const handleBack = () => router.push('/account/login')
  const handleEmail = (email: string) => setValues({ ...values, email })
  const handleUsername = (username: string) => setValues({ ...values, username })
  const handleNickname = (nickname: string) => setValues({ ...values, nickname })
  const handleLastName = (lastName: string) => setValues({ ...values, lastName })
  const handleFirstName = (firstName: string) => setValues({ ...values, firstName })
  const handlePassword1 = (password1: string) => setValues({ ...values, password1 })
  const handlePassword2 = (password2: string) => setValues({ ...values, password2 })
  const handleYear = (year: string) => setValues({ ...values, year: Number(year) })
  const handleMonth = (month: string) => setValues({ ...values, month: Number(month) })
  const handleDay = (day: string) => setValues({ ...values, day: Number(day) })
  const handleGender = (e: React.ChangeEvent<HTMLInputElement>) => setValues({ ...values, gender: e.target.value as Gender })

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

          <p className="mb_8">名前</p>
          <div className="name_group">
            <Input type="text" placeholder="姓" maxLength={30} required={isRequired} onChange={handleLastName} />
            <Input type="text" placeholder="名" maxLength={30} required={isRequired} onChange={handleFirstName} />
          </div>

          <Input type="text" placeholder="ユーザー名(英数字)" maxLength={20} className="mb_16" required={isRequired} onChange={handleUsername} />
          <Input type="text" placeholder="投稿者名" maxLength={80} className="mb_16" required={isRequired} onChange={handleNickname} />
          <Input type="email" placeholder="メールアドレス" maxLength={255} className="mb_16" required={isRequired} onChange={handleEmail} />
          <Input type="password" placeholder="パスワード(英数字8~16文字)" minLength={8} maxLength={16} className="mb_16" required={isRequired} onChange={handlePassword1} />
          <Input type="password" placeholder="パスワード(確認用)" minLength={8} maxLength={16} className="mb_16" required={isRequired} onChange={handlePassword2} />

          <p className="mb_8">生年月日</p>
          <div className="birthday_group mb_24">
            <Select value={values.year} options={selectDate.years} placeholder="年" onChange={handleYear} />
            <Select value={values.month} options={selectDate.months} placeholder="月" onChange={handleMonth} />
            <Select value={values.day} options={selectDate.days} placeholder="日" onChange={handleDay} />
          </div>

          <p className="mb_8">性別</p>
          <div className="td_gender mb_40">
            {genders.map((gender) => (
              <div key={gender.value} className="gender_radio">
                <input type="radio" value={gender.value} checked={gender.value === values.gender} id={`gender_${gender.value}`} onChange={handleGender} />
                <label htmlFor={`gender_${gender.value}`}>{gender.key}</label>
              </div>
            ))}
          </div>

          <Button color="green" size="l" name="アカウント登録" type="submit" className="w_full mb_24" loading={isLoading} onClick={handleSubmit} />
          <Button color="blue" size="l" name="戻る" className="w_full mb_24" onClick={handleBack} />
        </form>
        <Footer />
      </article>
      <Footer />
    </Main>
  )
}
