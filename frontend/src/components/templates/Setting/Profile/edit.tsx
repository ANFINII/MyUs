import { useState, ChangeEvent } from 'react'
import { useRouter } from 'next/router'
import { getAddressForm } from 'api/address'
import { getProfile, postProfile } from 'api/user'
import { ProfileIn, ProfileOut } from 'types/internal/auth'
import { prefectures } from 'utils/constants/address'
import { isEmpty } from 'utils/constants/common'
import { Gender } from 'utils/constants/enum'
import { selectDate } from 'utils/functions/datetime'
import { genders } from 'utils/functions/user'
import { useUser } from 'components/hooks/useUser'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import IconPerson from 'components/parts/Icon/Person'
import Input from 'components/parts/Input'
import InputImage from 'components/parts/Input/Imge'
import Select from 'components/parts/Input/Select'
import Textarea from 'components/parts/Input/Textarea'
import LoginRequired from 'components/parts/LoginRequired'
import Table from 'components/parts/Table'
import TableRow from 'components/parts/Table/Row'

interface Props {
  profile: ProfileOut
}

export default function SettingProfileEdit(props: Props) {
  const { profile } = props

  const router = useRouter()
  const { setUser } = useUser()
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [isRequired, setIsRequired] = useState<boolean>(false)
  const [message, setMessage] = useState<string>('')
  const [avatar, setAvatar] = useState<File>()
  const [values, setValues] = useState<ProfileOut>(profile)
  const { years, months, days } = selectDate()

  const handleBack = () => router.push('/setting/profile')
  const handleAvatar = (files: File | File[]) => Array.isArray(files) || setAvatar(files)
  const handleEmail = (email: string) => setValues({ ...values, email })
  const handleUsername = (username: string) => setValues({ ...values, username })
  const handleNickname = (nickname: string) => setValues({ ...values, nickname })
  const handleLastName = (lastName: string) => setValues({ ...values, lastName })
  const handleFirstName = (firstName: string) => setValues({ ...values, firstName })
  const handleYear = (year: string) => setValues({ ...values, year: Number(year) })
  const handleMonth = (month: string) => setValues({ ...values, month: Number(month) })
  const handleDay = (day: string) => setValues({ ...values, day: Number(day) })
  const handleGender = (e: ChangeEvent<HTMLInputElement>) => setValues({ ...values, gender: e.target.value as Gender })
  const handlePhone = (phone: string) => setValues({ ...values, phone })
  const handlePostalCode = (postalCode: string) => setValues({ ...values, postalCode })
  const handlePrefecture = (prefecture: string) => setValues({ ...values, prefecture })
  const handleCity = (city: string) => setValues({ ...values, city })
  const handleStreet = (street: string) => setValues({ ...values, street })
  const handleBuilding = (building: string) => setValues({ ...values, building })
  const handleIntroduction = (introduction: string) => setValues({ ...values, introduction })

  const handleAutoAddress = async () => {
    const address = await getAddressForm(values.postalCode)
    setValues({ ...values, prefecture: address.address1, city: address.address2, street: address.address3, building: '' })
  }

  const handlSubmit = async () => {
    const { email, username, nickname, lastName, firstName, phone, postalCode, prefecture } = values
    if (!(email && username && nickname && lastName && firstName && phone && postalCode && prefecture)) {
      setIsRequired(true)
      return
    }
    setIsLoading(true)
    await new Promise((resolve) => setTimeout(resolve, 1000))
    const request: ProfileIn = { ...values, avatar }
    try {
      const data = await postProfile(request)
      if (data?.message) {
        setMessage(data.message)
        return
      }
      const profile = await getProfile()
      setUser((prev) => ({ ...prev, avatar: profile.avatar }))
      setIsRequired(false)
      handleBack()
    } catch (e) {
      setMessage('エラーが発生しました！')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Main title="アカウント設定" type="table">
      <LoginRequired isAuth={!isEmpty(values)}>
        <div className="button_group">
          <Button color="green" size="s" name="登録" loading={isLoading} onClick={handlSubmit} />
          <Button color="blue" size="s" name="戻る" onClick={handleBack} />
        </div>

        {message && (
          <ul className="messages_profile">
            <li>{message}</li>
          </ul>
        )}

        <Table>
          <TableRow label="アカウント画像" className="table_header">
            <InputImage id="avatar" className="account_image_edit" icon={<IconPerson size="3.5em" type="square" />} onChange={handleAvatar} />
          </TableRow>
          <TableRow label="メールアドレス">
            <Input value={values.email} maxLength={120} required={isRequired} onChange={handleEmail} />
          </TableRow>
          <TableRow label="ユーザー名">
            <Input value={values.username} maxLength={30} placeholder="英数字" required={isRequired} onChange={handleUsername} />
          </TableRow>
          <TableRow label="投稿者名">
            <Input value={values.nickname} maxLength={60} required={isRequired} onChange={handleNickname} />
          </TableRow>
          <TableRow label="名前">
            <div className="td_name">
              <Input value={values.lastName} placeholder="姓" maxLength={30} required={isRequired} onChange={handleLastName} />
              <Input value={values.firstName} placeholder="名" maxLength={30} required={isRequired} onChange={handleFirstName} />
            </div>
          </TableRow>
          <TableRow label="生年月日">
            <div className="td_birthday">
              <Select value={values.year} options={years} placeholder="年" onChange={handleYear} />
              <Select value={values.month} options={months} placeholder="月" onChange={handleMonth} />
              <Select value={values.day} options={days} placeholder="日" onChange={handleDay} />
            </div>
          </TableRow>
          <TableRow isIndent label="年齢">
            {values.age}歳
          </TableRow>
          <TableRow label="性別">
            <div className="td_gender">
              {genders.map((gender) => (
                <div key={gender.value} className="gender_radio">
                  <input type="radio" value={gender.value} checked={gender.value === values.gender} id={`gender_${gender.value}`} onChange={handleGender} />
                  <label htmlFor={`gender_${gender.value}`}>{gender.key}</label>
                </div>
              ))}
            </div>
          </TableRow>
          <TableRow label="電話番号">
            <Input type="tel" value={values.phone} maxLength={15} required={isRequired} onChange={handlePhone} />
          </TableRow>
          <TableRow label="郵便番号">
            <div className="d_flex">
              <Input type="tel" value={values.postalCode} maxLength={8} className="mr_2" required={isRequired} onChange={handlePostalCode} />
              <Button name="住所自動入力" onClick={handleAutoAddress} />
            </div>
          </TableRow>
          <TableRow label="住所">
            <div className="td_location">
              <Select value={values.prefecture} options={prefectures} placeholder="都道府県" onChange={handlePrefecture} />
              <Input value={values.city} placeholder="市区町村" maxLength={255} onChange={handleCity} />
              <Input value={values.street} placeholder="町名番地" maxLength={255} onChange={handleStreet} />
              <Input value={values.building} placeholder="建物名" maxLength={255} onChange={handleBuilding} />
            </div>
          </TableRow>
          <TableRow label="自己紹介">
            <Textarea className="textarea_margin" defaultValue={values.introduction} onChange={handleIntroduction} />
          </TableRow>
        </Table>
      </LoginRequired>
    </Main>
  )
}
