import { useState, ChangeEvent } from 'react'
import Image from 'next/image'
import { useRouter } from 'next/router'
import { UserProfile } from 'types/internal/auth'
import { prefectures } from 'utils/constants/prefectures'
import { selectDate } from 'utils/functions/datetime'
import { genderMap, genders } from 'utils/functions/user'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import IconPerson from 'components/parts/Icon/Person'
import Input from 'components/parts/Input'
import Select from 'components/parts/Input/Select'
import Textarea from 'components/parts/Input/Textarea'
import LoginRequired from 'components/parts/LoginRequired'

interface Props {
  user: UserProfile
}

export default function Profile(props: Props) {
  const { user } = props

  const router = useRouter()
  const [isEdit, setIsEdit] = useState<boolean>(false)
  const [userGender, setUserGender] = useState<string>(user.gender)
  const { years, months, days } = selectDate()

  const handleEdit = () => setIsEdit(!isEdit)
  const handleGender = (e: ChangeEvent<HTMLInputElement>) => setUserGender(e.target.value)

  const handlSubmit = () => {
    router.push('/setting/profile')
  }

  return (
    <Main title="アカウント設定" type="table">
      <LoginRequired isAuth={!!user}>
        {isEdit ? (
          <div className="button_group">
            <Button green size="xs" type="submit" name="登録" onClick={handlSubmit} />
            <Button blue size="xs" name="戻る" onClick={handleEdit} />
          </div>
        ) : (
          <div className="button_group">
            <Button blue size="xs" name="編集" onClick={handleEdit} />
            <Button blue size="xs" name="パスワード変更" onClick={() => router.push('/setting/password/change')} />
          </div>
        )}

        {isEdit ? (
          <table className="table">
            <tbody>
              <tr className="table_header">
                <td className="td_color">アカウント画像</td>
                <td valign="baseline">
                  <label htmlFor="account_image_input" className="update_account_image">
                    <IconPerson size="3.5em" type="square" />
                    <input type="file" name="image" accept="image/*" id="account_image_input" className="custom-file-input" />
                  </label>
                </td>
              </tr>
              <tr>
                <td className="td_color">メールアドレス</td>
                <td>
                  <Input type="text" name="email" value={user.email} maxLength={120} />
                </td>
              </tr>
              <tr>
                <td className="td_color">ユーザー名</td>
                <td>
                  <Input type="text" name="username" value={user.username} maxLength={30} placeholder="英数字" />
                </td>
              </tr>
              <tr>
                <td className="td_color">投稿者名</td>
                <td>
                  <Input type="text" name="nickname" value={user.nickname} maxLength={60} />
                </td>
              </tr>
              <tr>
                <td className="td_color">名前</td>
                <td>
                  <div className="td_name">
                    <Input type="text" name="last_name" value={user.lastname} placeholder="姓" maxLength={30} />
                    <Input type="text" name="first_name" value={user.firstname} placeholder="名" maxLength={30} />
                  </div>
                </td>
              </tr>
              <tr>
                <td className="td_color">生年月日</td>
                <td>
                  <div className="td_birthday">
                    <Select name="year" value={user.year} options={years} placeholder="年" />
                    <Select name="month" value={user.month} options={months} placeholder="月" />
                    <Select name="day" value={user.day} options={days} placeholder="日" />
                  </div>
                </td>
              </tr>
              <tr>
                <td className="td_color">年齢</td>
                <td className="td_indent">{user.age}歳</td>
              </tr>
              <tr>
                <td className="td_color">性別</td>
                <td className="td_gender">
                  <div className="gender">
                    {genders.map((gender) => (
                      <div key={gender.value} className="gender">
                        <input type="radio" name="gender" value={gender.value} checked={gender.value === userGender} id={`gender_${gender.value}`} onChange={handleGender} />
                        <label htmlFor={`gender_${gender.value}`}>{gender.key}</label>
                      </div>
                    ))}
                  </div>
                </td>
              </tr>
              <tr>
                <td className="td_color">電話番号</td>
                <td>
                  <Input type="tel" name="phone" value={user.phone} maxLength={15} required />
                </td>
              </tr>
              <tr>
                <td className="td_color">郵便番号</td>
                <td>
                  <Input type="tel" name="postal_code" value={user.postalCode} maxLength={8} required />
                </td>
              </tr>
              <tr>
                <td className="td_color">住所</td>
                <td className="td_location">
                  <Select name="year" value={user.prefecture} options={prefectures} placeholder="都道府県" />
                  <Input type="text" name="city" value={user.city} placeholder="市区町村" maxLength={255} />
                  <Input type="text" name="address" value={user.address} placeholder="丁番地" maxLength={255} />
                  <Input type="text" name="building" value={user.building} placeholder="建物名" maxLength={255} />
                </td>
              </tr>
              <tr>
                <td className="td_color">自己紹介</td>
                <td>
                  <Textarea name="introduction" className="textarea_margin">
                    {user.introduction}
                  </Textarea>
                </td>
              </tr>
            </tbody>
          </table>
        ) : (
          <table className="table">
            <tbody>
              <tr>
                <td className="td_color td-header">アカウント画像</td>
                <td>
                  <label htmlFor="account_image_input" className="account_image">
                    <a href={user.avatar} data-lightbox="group">
                      <Image src={user.avatar} title={user.nickname} width={56} height={56} alt="" data-lightbox="group" />
                    </a>
                  </label>
                </td>
              </tr>
              <tr>
                <td className="td_color">メールアドレス</td>
                <td className="td_indent">{user.email}</td>
              </tr>
              <tr>
                <td className="td_color">ユーザー名</td>
                <td className="td_indent">{user.username}</td>
              </tr>
              <tr>
                <td className="td_color">投稿者名</td>
                <td className="td_indent">{user.nickname}</td>
              </tr>
              <tr>
                <td className="td_color">名前</td>
                <td className="td_indent">{user.fullname}</td>
              </tr>
              <tr>
                <td className="td_color">生年月日</td>
                <td className="td_indent">
                  {user.year}年{user.month}月{user.day}日
                </td>
              </tr>
              <tr>
                <td className="td_color">年齢</td>
                <td className="td_indent">{user.age}歳</td>
              </tr>
              <tr>
                <td className="td_color">性別</td>
                <td className="td_indent">{genderMap[user.gender]}</td>
              </tr>
              <tr>
                <td className="td_color">電話番号</td>
                <td className="td_indent">{user.phone}</td>
              </tr>
              <tr>
                <td className="td_color">郵便番号</td>
                <td className="td_indent">{user.postalCode}</td>
              </tr>
              <tr>
                <td className="td_color">住所</td>
                <td className="td_indent">
                  {user.prefecture} {user.city}
                  {user.address} {user.building}
                </td>
              </tr>
              <tr>
                <td className="td_color">自己紹介</td>
                <td className="td_indent">{user.introduction}</td>
              </tr>
            </tbody>
          </table>
        )}
      </LoginRequired>
    </Main>
  )
}
