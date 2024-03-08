import { useState, ChangeEvent } from 'react'
import Image from 'next/image'
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

interface Props {
  user: UserProfile
}

export default function SettingProfile(props: Props) {
  const { user } = props

  const router = useRouter()
  const [isEdit, setIsEdit] = useState<boolean>(false)
  const { years, months, days } = selectDate()
  const [message, setMessage] = useState<string>('')
  const [data, setData] = useState<UserProfile>(user)

  const reset = () => setData(user)
  const handleEdit = () => setIsEdit(!isEdit)
  const handleEmail = (email: string) => setData({ ...data, email })
  const handleUsername = (username: string) => setData({ ...data, username })
  const handleNickname = (nickname: string) => setData({ ...data, nickname })
  const handleLastname = (lastname: string) => setData({ ...data, lastname })
  const handleFirstname = (firstname: string) => setData({ ...data, firstname })
  const handleYear = (year: string) => setData({ ...data, year: Number(year) })
  const handleMonth = (month: string) => setData({ ...data, month: Number(month) })
  const handleDay = (day: string) => setData({ ...data, day: Number(day) })
  const handleGender = (e: ChangeEvent<HTMLInputElement>) => setData({ ...data, gender: e.target.value as Gender })
  const handlePhone = (phone: string) => setData({ ...data, phone })
  const handlePostalCode = (postalCode: string) => setData({ ...data, postalCode })
  const handlePrefecture = (prefecture: string) => setData({ ...data, prefecture })
  const handleCity = (city: string) => setData({ ...data, city })
  const handleStreet = (street: string) => setData({ ...data, street })
  const handleBuilding = (building: string) => setData({ ...data, building })
  const handleIntroduction = (introduction: string) => setData({ ...data, introduction })

  const handleBack = () => {
    reset()
    handleEdit()
  }

  const handleAutoAddress = async () => {
    const address = await getAddressForm(data.postalCode)
    setData({ ...data, prefecture: address.address1, city: address.address2, street: address.address3, building: '' })
  }

  const handlSubmit = async () => {
    try {
      const resData = await postProfile(data)
      resData?.message ? setMessage(resData.message) : handleEdit()
    } catch (e) {
      setMessage('エラーが発生しました！')
    }
  }

  return (
    <Main title="アカウント設定" type="table">
      <LoginRequired isAuth={!isEmpty(data)}>
        {isEdit ? (
          <div className="button_group">
            <Button color="green" size="s" name="登録" onClick={handlSubmit} />
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
                <input type="file" name="image" accept="image/*" id="account_image_input" className="custom-file-input" />
              </label>
            </TableRow>
            <TableRow label="メールアドレス">
              <Input type="text" name="email" value={data.email} maxLength={120} onChange={handleEmail} />
            </TableRow>
            <TableRow label="ユーザー名">
              <Input type="text" name="username" value={data.username} maxLength={30} placeholder="英数字" onChange={handleUsername} />
            </TableRow>
            <TableRow label="投稿者名">
              <Input type="text" name="nickname" value={data.nickname} maxLength={60} onChange={handleNickname} />
            </TableRow>
            <TableRow label="名前">
              <div className="td_name">
                <Input type="text" name="last_name" value={data.lastname} placeholder="姓" maxLength={30} onChange={handleLastname} />
                <Input type="text" name="first_name" value={data.firstname} placeholder="名" maxLength={30} onChange={handleFirstname} />
              </div>
            </TableRow>
            <TableRow label="生年月日">
              <div className="td_birthday">
                <Select name="year" value={data.year} options={years} placeholder="年" onChange={handleYear} />
                <Select name="month" value={data.month} options={months} placeholder="月" onChange={handleMonth} />
                <Select name="day" value={data.day} options={days} placeholder="日" onChange={handleDay} />
              </div>
            </TableRow>
            <TableRow isIndent label="年齢">
              {data.age}歳
            </TableRow>
            <TableRow label="性別">
              <div className="td_gender">
                {genders.map((gender) => (
                  <div key={gender.value} className="gender_radio">
                    <input type="radio" name="gender" value={gender.value} checked={gender.value === data.gender} id={`gender_${gender.value}`} onChange={handleGender} />
                    <label htmlFor={`gender_${gender.value}`}>{gender.key}</label>
                  </div>
                ))}
              </div>
            </TableRow>
            <TableRow label="電話番号">
              <Input type="tel" name="phone" value={data.phone} maxLength={15} onChange={handlePhone} required />
            </TableRow>
            <TableRow label="郵便番号">
              <div className="d_flex">
                <Input type="tel" name="postal_code" value={data.postalCode} maxLength={8} className="mr_2" onChange={handlePostalCode} required />
                <Button name="住所自動入力" onClick={handleAutoAddress} />
              </div>
            </TableRow>
            <TableRow label="住所">
              <div className="td_location">
                <Select name="year" value={data.prefecture} options={prefectures} placeholder="都道府県" onChange={handlePrefecture} />
                <Input type="text" name="city" value={data.city} placeholder="市区町村" maxLength={255} onChange={handleCity} />
                <Input type="text" name="street" value={data.street} placeholder="町名番地" maxLength={255} onChange={handleStreet} />
                <Input type="text" name="building" value={data.building} placeholder="建物名" maxLength={255} onChange={handleBuilding} />
              </div>
            </TableRow>
            <TableRow label="自己紹介">
              <Textarea name="introduction" className="textarea_margin" onChange={handleIntroduction}>
                {data.introduction}
              </Textarea>
            </TableRow>
          </Table>
        ) : (
          <Table>
            <TableRow label="アカウント画像" className="table_header">
              <label htmlFor="account_image_input" className="account_image">
                <a href={data.avatar} data-lightbox="group">
                  <Image src={data.avatar} title={data.nickname} width={56} height={56} alt="" data-lightbox="group" />
                </a>
              </label>
            </TableRow>
            <TableRow isIndent label="メールアドレス">
              {data.email}
            </TableRow>
            <TableRow isIndent label="ユーザー名">
              {data.username}
            </TableRow>
            <TableRow isIndent label="投稿者名">
              {data.nickname}
            </TableRow>
            <TableRow isIndent label="名前">
              {data.fullname}
            </TableRow>
            <TableRow isIndent label="生年月日">
              {data.year}年{data.month}月{data.day}日
            </TableRow>
            <TableRow isIndent label="年齢">
              {data.age}歳
            </TableRow>
            <TableRow isIndent label="性別">
              {genderMap[data.gender]}
            </TableRow>
            <TableRow isIndent label="電話番号">
              {data.phone}
            </TableRow>
            <TableRow isIndent label="郵便番号">
              {data.postalCode}
            </TableRow>
            <TableRow isIndent label="住所">
              {data.prefecture} {data.city}
              {data.street} {data.building}
            </TableRow>
            <TableRow isIndent label="自己紹介">
              {data.introduction}
            </TableRow>
          </Table>
        )}
      </LoginRequired>
    </Main>
  )
}
