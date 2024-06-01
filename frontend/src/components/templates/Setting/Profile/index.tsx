import { useState, ChangeEvent } from 'react'
import { useRouter } from 'next/router'
import { getAddressForm } from 'api/address'
import { postProfile } from 'api/user'
import { UserProfile } from 'types/internal/auth'
import { prefectures } from 'utils/constants/address'
import { isEmpty } from 'utils/constants/common'
import { Gender } from 'utils/constants/enum'
import { selectDate } from 'utils/functions/datetime'
import { genderMap, genders } from 'utils/functions/user'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import IconPerson from 'components/parts/Icon/Person'
import Input from 'components/parts/Input'
import Select from 'components/parts/Input/Select'
import Textarea from 'components/parts/Input/Textarea'
import LoginRequired from 'components/parts/LoginRequired'
import Table from 'components/parts/Table'
import TableRow from 'components/parts/Table/Row'
import LightBox from 'components/widgets/LightBox'

interface Props {
  user: UserProfile
}

export default function SettingProfile(props: Props) {
  const { user } = props

  const router = useRouter()
  const [isEdit, setIsEdit] = useState<boolean>(false)
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [isRequired, setIsRequired] = useState<boolean>(false)
  const { years, months, days } = selectDate()
  const [message, setMessage] = useState<string>('')
  const [values, setValues] = useState<UserProfile>(user)

  const reset = () => setValues(user)
  const handleEdit = () => setIsEdit(!isEdit)
  const handleEmail = (email: string) => setValues({ ...values, email })
  const handleUsername = (username: string) => setValues({ ...values, username })
  const handleNickname = (nickname: string) => setValues({ ...values, nickname })
  const handleLastname = (lastname: string) => setValues({ ...values, lastname })
  const handleFirstname = (firstname: string) => setValues({ ...values, firstname })
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

  const handleBack = () => {
    reset()
    handleEdit()
    setIsRequired(false)
  }

  const handleAutoAddress = async () => {
    const address = await getAddressForm(values.postalCode)
    setValues({ ...values, prefecture: address.address1, city: address.address2, street: address.address3, building: '' })
  }

  const handlSubmit = async () => {
    const { email, username, nickname, lastname, firstname, phone, postalCode } = values
    if (!(email && username && nickname && lastname && firstname && phone && postalCode)) {
      setIsRequired(true)
      return
    }
    setIsLoading(true)
    await new Promise((resolve) => setTimeout(resolve, 1000))
    try {
      const data = await postProfile(values)
      data?.message ? setMessage(data.message) : handleEdit()
      handleEdit()
      setIsRequired(false)
    } catch (e) {
      setMessage('エラーが発生しました！')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Main title="アカウント設定" type="table">
      <LoginRequired isAuth={!isEmpty(values)}>
        {isEdit ? (
          <div className="button_group">
            <Button color="green" size="s" name="登録" loading={isLoading} onClick={handlSubmit} />
            <Button color="blue" size="s" name="戻る" onClick={handleBack} />
          </div>
        ) : (
          <div className="button_group">
            <Button color="blue" size="s" name="編集" onClick={handleEdit} />
            <Button color="blue" size="s" name="パスワード変更" onClick={() => router.push('/setting/password/change')} />
          </div>
        )}

        {message && (
          <ul className="messages_profile">
            <li>{message}</li>
          </ul>
        )}

        {isEdit ? (
          <Table>
            <TableRow label="アカウント画像" className="table_header">
              <label htmlFor="account_image_input" className="update_account_image">
                <IconPerson size="3.5em" type="square" />
                <input type="file" accept="image/*" id="account_image_input" className="custom-file-input" />
                {/* <InputFile label="音楽" accept="image/*" onChange={handleFile} /> */}
              </label>
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
                <Input value={values.lastname} placeholder="姓" maxLength={30} required={isRequired} onChange={handleLastname} />
                <Input value={values.firstname} placeholder="名" maxLength={30} required={isRequired} onChange={handleFirstname} />
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
              <Textarea className="textarea_margin" value={values.introduction} onChange={handleIntroduction}>
                {values.introduction}
              </Textarea>
            </TableRow>
          </Table>
        ) : (
          <Table>
            <TableRow label="アカウント画像" className="table_header">
              <label htmlFor="account_image_input" className="account_image">
                <LightBox size="56" src={values.avatar} title={values.nickname} />
              </label>
            </TableRow>
            <TableRow isIndent label="メールアドレス">
              {values.email}
            </TableRow>
            <TableRow isIndent label="ユーザー名">
              {values.username}
            </TableRow>
            <TableRow isIndent label="投稿者名">
              {values.nickname}
            </TableRow>
            <TableRow isIndent label="名前">
              {values.fullname}
            </TableRow>
            <TableRow isIndent label="生年月日">
              {values.year}年{values.month}月{values.day}日
            </TableRow>
            <TableRow isIndent label="年齢">
              {values.age}歳
            </TableRow>
            <TableRow isIndent label="性別">
              {genderMap[values.gender]}
            </TableRow>
            <TableRow isIndent label="電話番号">
              {values.phone}
            </TableRow>
            <TableRow isIndent label="郵便番号">
              {values.postalCode}
            </TableRow>
            <TableRow isIndent label="住所">
              {values.prefecture} {values.city}
              {values.street} {values.building}
            </TableRow>
            <TableRow isIndent label="自己紹介">
              {values.introduction}
            </TableRow>
          </Table>
        )}
      </LoginRequired>
    </Main>
  )
}
