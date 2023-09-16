import Router from 'next/router'
import { Profile } from 'types/auth'
import { prefectures } from 'utils/constants/prefectures'
import { selectDate } from 'utils/functins/datetime'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import IconPerson from 'components/parts/Icon/Person'
import Input from 'components/parts/Input'
import Select from 'components/parts/Input/Select'
import Textarea from 'components/parts/Input/Textarea'

interface Props {
  user: Profile
}

export default function ProfileUpdate(props: Props) {
  const { user } = props

  const { years, months, days } = selectDate()

  return (
    <Main title="MyUsアカウント設定">
      {user ? (
        <article className="article_table">
          <h1>アカウント設定</h1>
          {/* {% if messages %}
          <ul className="messages_profile">
            {% for message in messages %}
            <li {% if message.tags %} className={message.tags } {% endif %}>{{message }}</li><br>
            {% endfor %}
          </ul>
          {% endif %} */}

          <div className="button_group">
            <Button green size="xs" type="submit" name="登録" />
            <Button blue size="xs" name="戻る" onClick={() => Router.push('/setting/profile')} />
          </div>

          <table className="table">
            <tbody>
              <tr className="table_header">
                <td className="td_color">アカウント画像</td>
                <td valign="baseline">
                  <label htmlFor="account_image_input" className="update_account_image">
                    <IconPerson />
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
                    <input
                      type="radio"
                      name="gender"
                      value={user.key}
                      id={`gender_${user.key}`}
                      className=""
                      // {user.gender === user.key && defaultChecked="checked" }
                    />
                    <label htmlFor={`gender_${user.key}`} className="custom-control-label">
                      {user.gender}
                    </label>
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
          <Footer />
        </article>
      ) : (
        <article className="article_table">
          <h1>アカウント設定</h1>
          <h2 className="login_required">ログインしてください</h2>
        </article>
      )}
    </Main>
  )
}
