

import Router from 'next/router'
import {ProfileResponse} from 'utils/type'
import SelectDate from 'utils/lib/SelectDate'
import useSelectDate from 'utils/lib/SelectPrefecture'
import Main from 'components/layouts/Main'
import Footer from 'components/layouts/Footer'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import Select from 'components/parts/Input/Select'
import Textarea from 'components/parts/Input/Textarea'

interface Props {user: ProfileResponse}

export default function ProfileUpdate(props: Props) {
  const {user} = props
  const {years, months, days} = SelectDate()
  const prefectures = useSelectDate()

  return (
    <Main title="MyUsアカウント設定">
      {user ?
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
            <Button green size="xs" type="submit">登録</Button>
            <Button blue size="xs" onClick={() => Router.push('/setting/profile')}>戻る</Button>
          </div>

          <table className="table">
            <tbody>
              <tr className="table_header"><td className="td_color">アカウント画像</td>
                <td valign="baseline">
                  <label htmlFor="account_image_input" className="update_account_image">
                    <svg xmlns="http://www.w3.org/2000/svg" width="3.5em" height="3.5em" fill="currentColor" className="bi bi-person-square" viewBox="0 0 16 16">
                      <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"/>
                      <path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm12 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1v-1c0-1-1-4-6-4s-6 3-6 4v1a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12z"/>
                    </svg>
                    <input type="file" name="image" accept="image/*" id="account_image_input" className="custom-file-input" />
                  </label>
                </td>
              </tr>
              <tr><td className="td_color">メールアドレス</td><td><Input type="text" name="email" value={user.email} maxLength={120} /></td></tr>
              <tr><td className="td_color">ユーザー名</td><td><Input type="text" name="username" value={user.username} maxLength={30} placeholder="英数字" /></td></tr>
              <tr><td className="td_color">投稿者名</td><td><Input type="text" name="nickname" value={user.nickname} maxLength={60} /></td></tr>
              <tr><td className="td_color">名前</td>
                <td>
                  <div className="td_name">
                    <Input type="text" name="last_name" value={user.lastname} placeholder="姓" maxLength={30} />
                    <Input type="text" name="first_name" value={user.firstname} placeholder="名" maxLength={30} />
                  </div>
                </td>
              </tr>
              <tr><td className="td_color">生年月日</td>
                <td>
                  <div className="td_birthday">
                    <Select name="year" value={user.year} options={years} placeholder="年" />
                    <Select name="month" value={user.month} options={months} placeholder="月" />
                    <Select name="day" value={user.day} options={days} placeholder="日" />
                  </div>
                </td>
              </tr>
              <tr><td className="td_color">年齢</td><td className="td_indent">{user.age}歳</td></tr>
              <tr>
                <td className="td_color">性別</td>
                <td className="td_gender">
                  <div className="gender">
                    <input type="radio" name="gender" value={user.key} id={`gender_${user.key}`} className=""
                    // {user.gender === user.key && defaultChecked="checked" }
                    />
                    <label htmlFor={`gender_${user.key}`} className="custom-control-label">{user.gender}</label>
                  </div>
                </td>
              </tr>
              <tr><td className="td_color">電話番号</td><td><Input type="tel" name="phone" value={user.phone} maxLength={15} required /></td></tr>
              <tr><td className="td_color">郵便番号</td><td><Input type="tel" name="postal_code" value={user.postal_code} maxLength={8} required /></td></tr>
              <tr><td className="td_color">住所</td>
                <td className="td_location">
                  <Select name="year" value={user.prefecture} options={prefectures} placeholder="都道府県" />
                  <Input type="text" name="city" value={user.city} placeholder="市区町村" maxLength={255} />
                  <Input type="text" name="address" value={user.address} placeholder="丁番地" maxLength={255} />
                  <Input type="text" name="building" value={user.building} placeholder="建物名" maxLength={255} />
                </td>
              </tr>
              <tr>
                <td className="td_color">自己紹介</td>
                <td><Textarea name="introduction" className="textarea_margin">{user.introduction}</Textarea></td>
              </tr>
            </tbody>
          </table>
          <Footer />
        </article>
      :
        <article className="article_table">
          <h1>アカウント設定</h1>
          <h2 className="login_required">ログインしてください</h2>
        </article>
      }
    </Main>
  )
}
