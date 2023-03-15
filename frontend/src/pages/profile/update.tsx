

import {GetServerSideProps} from 'next'
import Head from 'next/head'
import Link from 'next/link'
import Router from 'next/router'
import {ProfileResponse} from 'utils/type'
import Footer from 'components/layouts/Footer'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import Textarea from 'components/parts/Input/Textarea'

// export const getServerSideProps: GetServerSideProps = async (context) => {
//  const cookie = context.req?.headers.cookie
//  const res = await axios.get('/api/profile', {
//   headers: {cookie: cookie!}
//  })
//  const data: ProfileResponse = res.data
//  return {
//   props: {user: data}
//  }
// }

export default function ProfileUpdate() {
  const user: ProfileResponse = {
    "avatar": "/media/users/images_user/user_5/MyUs_Profile_01.jpg",
    "email": "anfinii56@gmail.com",
    "username": "anfinii56",
    "nickname": "アン",
    "fullname": "翁 安",
    "lastname": "翁",
    "firstname": "安",
    "year": 1987,
    "month": 5,
    "day": 6,
    "age": 35,
    "gender": "男性",
    "phone": "090-9678-8552",
    "country_code": "JP",
    "postal_code": "210-0844",
    "prefecture": "神奈川県",
    "city": "川崎市川崎区渡田新町",
    "address": "1-10-8-1",
    "building": "MyUsビル 56F",
    "introduction": "MyUs開発者、ユーザー用"
  }
  const handleClick = () => Router.push('/profile')

  return (
    <>
      <Head>
        <title>MyUsアカウント設定</title>
      </Head>

      {user ?
        <article className="article_account">
          <h1>アカウント設定</h1>
          {/* {% if messages %}
          <ul className="messages_profile">
            {% for message in messages %}
            <li {% if message.tags %} className={message.tags } {% endif %}>{{message }}</li><br>
            {% endfor %}
          </ul>
          {% endif %} */}

          <div className="btn-column">
            <div className="btn-column1">
              <Button green size="xs" type="submit">登録</Button>
            </div>
            <div className="btn-column2">
              <Button blue size="xs" onClick={handleClick}>戻る</Button>
            </div>
          </div>

          <table className="table">
            <tbody>
              <tr className="table_header"><td className="td-color">アカウント画像</td>
                <td valign="baseline">
                  <label htmlFor="account_image_input" className="update_account_image">
                    <svg xmlns="http://www.w3.org/2000/svg" width="3.5em" height="3.5em" fill="currentColor" className="bi bi-person-square" viewBox="0 0 16 16">
                      <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"/>
                      <path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm12 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1v-1c0-1-1-4-6-4s-6 3-6 4v1a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12z"/>
                    </svg>
                    <input type="file" name="image" accept="image/*" id="account_image_input" className="custom-file-input"/>
                  </label>
                </td>
              </tr>
              <tr><td className="td-color">メールアドレス</td><td><Input type="text" name="email" value={user.email} maxLength={120}/></td></tr>
              <tr><td className="td-color">ユーザー名</td><td><Input type="text" name="username" value={user.username} maxLength={30} placeholder="英数字"/></td></tr>
              <tr><td className="td-color">投稿者名</td><td><Input type="text" name="nickname" value={user.nickname} maxLength={60}/></td></tr>
              <tr><td className="td-color">名前</td>
                <td>
                  <div className="td-name">
                    <Input type="text" name="last_name" value={user.lastname} id="last_name" placeholder="姓" maxLength={30}/>
                    <Input type="text" name="first_name" value={user.firstname} id="first_name" placeholder="名" maxLength={30}/>
                  </div>
                </td>
              </tr>
              <tr><td className="td-color">生年月日</td>
                <td>
                  <div className="td-birthday">
                    <select name="year" id="year">
                      <option value={user.year} style={{display: 'none'}}>{user.year}</option>
                    </select>
                    <select name="month" id="month">
                      <option value={user.month} style={{display: 'none'}}>{user.month}</option>
                    </select>
                    <select name="day" id="day">
                      <option value={user.day} style={{display: 'none'}}>{user.day}</option>
                    </select>
                  </div>
                </td>
              </tr>
              <tr><td className="td-color">年齢</td><td className="td-indent">{user.age}歳</td></tr>
              <tr>
                <td className="td-color">性別</td>
                <td className="td-gender">
                  <div className="td_gender">
                    <input type="radio" name="gender" value={user.key} id={`gender_${user.key}`} className=""
                    // {user.gender === user.key && defaultChecked="checked" }
                    />
                    <label htmlFor={`gender_${user.key}`} className="custom-control-label">{user.gender}</label>
                  </div>
                </td>
              </tr>
              <tr><td className="td-color">電話番号</td><td><Input type="tel" name="phone" value={user.phone} maxLength={15} required/></td></tr>
              <tr><td className="td-color">郵便番号</td><td><Input type="tel" name="postal_code" value={user.postal_code} maxLength={8} required/></td></tr>
              <tr><td className="td-color">住所</td>
                <td className="td-location">
                  <select name="prefecture" id="prefecture" className="location1">
                    <option value="">都道府県</option>
                    <option value={user.prefecture} style={{display: 'none'}} selected>{user.prefecture }</option>
                  </select>
                  <Input type="text" name="city" value={user.city} placeholder="市区町村" maxLength={255} className="location2"/>
                  <Input type="text" name="address" value={user.address} placeholder="丁番地" maxLength={255} className="location3"/>
                  <Input type="text" name="building" value={user.building} placeholder="建物名" maxLength={255} className="location4"/>
                </td>
              </tr>
              <tr>
                <td className="td-color">自己紹介</td>
                <td><Textarea name="introduction" className="textarea_margin">{user.introduction}</Textarea></td>
              </tr>
            </tbody>
          </table>

          <Footer/>
        </article>
      :
        <article className="article_account">
          <h1>アカウント設定</h1>
          <h2 className="login_required">ログインしてください</h2>
        </article>
      }
    </>
  )
}
