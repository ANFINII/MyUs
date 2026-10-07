import { ChangeEvent, useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useSearch } from '@tanstack/react-router'
import { SignupIn } from 'types/internal/auth'
import { getSignupVerify, postSignup } from 'api/internal/auth'
import { FetchError, GenderType } from 'utils/constants/enum'
import { nowDate, selectDate } from 'utils/functions/datetime'
import { useAppRouter } from 'components/hooks/useAppRouter'
import { useLoading } from 'components/hooks/useLoading'
import { useRequired } from 'components/hooks/useRequired'
import { useToast } from 'components/hooks/useToast'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import Password from 'components/parts/Input/Password'
import Radio from 'components/parts/Input/Radio'
import SelectBox from 'components/parts/Input/SelectBox'
import HStack from 'components/parts/Stack/Horizontal'
import VStack from 'components/parts/Stack/Vertical'
import style from '../Account.module.scss'

const initSignup: SignupIn = {
  token: '',
  email: '',
  username: '',
  nickname: '',
  password1: '',
  password2: '',
  lastName: '',
  firstName: '',
  year: nowDate.year - 50,
  month: 6,
  day: 15,
  gender: GenderType.Male,
}

export default function Signup(): React.JSX.Element {
  const router = useAppRouter()
  const { t } = useTranslation()
  const { token } = useSearch({ strict: false })
  const { loading, handleLoading } = useLoading()
  const { error, validate } = useRequired()
  const { toast, handleToast } = useToast()
  const [values, setValues] = useState<SignupIn>(initSignup)
  const [isVerified, setIsVerified] = useState<boolean>(false)

  const { years, months, days } = selectDate()
  const handleBack = () => router.push('/account/login')
  const handleInput = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, [e.target.name]: e.target.value })
  const handleSelect = (e: ChangeEvent<HTMLSelectElement>) => setValues({ ...values, [e.target.name]: e.target.value })

  useEffect(() => {
    if (!token) {
      router.push('/account/login')
      return
    }
    const verify = async () => {
      const ret = await getSignupVerify(token)
      if (ret.isErr()) {
        router.push('/account/login')
        return
      }
      setValues((prev) => ({ ...prev, token, email: ret.value.email }))
      setIsVerified(true)
    }
    verify()
  }, [router, token])

  const handleSubmit = async () => {
    const { email, username, nickname, lastName, firstName, password1, password2 } = values
    if (!validate({ email, username, nickname, lastName, firstName, password1, password2 })) return
    handleLoading(true)
    const ret = await postSignup(values)
    handleLoading(false)
    if (ret.isErr()) {
      handleToast(FetchError.Post, true)
      return
    }
    handleBack()
  }

  return (
    <Main metaTitle={t('account.signup.title')} toast={toast}>
      <article className={style.account}>
        <form method="POST" action="" className={style.form}>
          <h1 className={style.signup_title}>{t('account.signup.title')}</h1>
          {isVerified && (
            <>
              <VStack gap="8">
                <VStack gap="4">
                  <p>{t('account.signup.name')}</p>
                  <div className="name_group">
                    <Input name="lastName" placeholder={t('account.signup.lastName')} maxLength={30} required error={error} onChange={handleInput} />
                    <Input name="firstName" placeholder={t('account.signup.firstName')} maxLength={30} required error={error} onChange={handleInput} />
                  </div>
                </VStack>

                <Input name="username" placeholder={t('account.signup.username')} maxLength={20} required error={error} onChange={handleInput} />
                <Input name="nickname" placeholder={t('account.signup.nickname')} maxLength={80} required error={error} onChange={handleInput} />
                <Input type="email" name="email" value={values.email} disabled maxLength={255} />
                <Password name="password1" placeholder={t('account.form.passwordNew')} error={error} onChange={handleInput} />
                <Password name="password2" placeholder={t('account.form.passwordConfirm')} error={error} onChange={handleInput} />

                <VStack gap="4">
                  <p>{t('account.signup.birthday')}</p>
                  <HStack gap="2" full>
                    <SelectBox name="year" value={String(values.year)} options={years} onChange={handleSelect} />
                    <SelectBox name="month" value={String(values.month)} options={months} onChange={handleSelect} />
                    <SelectBox name="day" value={String(values.day)} options={days} onChange={handleSelect} />
                  </HStack>
                </VStack>

                <VStack gap="4">
                  <p>{t('account.signup.gender')}</p>
                  <HStack gap="5">
                    {Object.entries(GenderType).map(([key, value]) => (
                      <Radio key={key} name="gender" label={t(`gender.${value}`)} value={value} checked={value === values.gender} onChange={handleInput} />
                    ))}
                  </HStack>
                </VStack>
              </VStack>

              <VStack gap="12" className="mv_40">
                <Button color="green" size="l" name={t('account.signup.submit')} type="submit" loading={loading} onClick={handleSubmit} />
                <Button color="blue" size="l" name={t('status.back')} onClick={handleBack} />
              </VStack>
            </>
          )}
        </form>
      </article>
      <Footer />
    </Main>
  )
}
