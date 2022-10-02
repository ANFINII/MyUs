import Head from 'next/head'
import Footer from 'components/layouts/footer'
import Link from 'next/link'
import axios from 'lib/api/axios'
import { useState, useEffect } from 'react'
import { userType, UserType } from 'lib/utils/type'

export default function Profile() {
  const [user, setUser] = useState<UserType>(userType)
  const auth = 200
  const url = process.env.NEXT_PUBLIC_API_URL
  const token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY1MDQ2NjA1LCJqdGkiOiIwNzI5ZjIwZjkwMGM0MzU3YmEwOWYxNzA5Y2QwZDMwNSIsInVzZXJfaWQiOjF9.QKL4zB8Grig3M8_gC1Sgh9NseZOYICy3q0jOBcpJCwU'

  useEffect(() => {
    axios.get(url + '/api/profile', {headers: {'Authorization': 'JWT ' + token}})
    .then(res => {setUser(res.data)})
    .catch(e => {
      console.log(e)
    })
  },[])

  if (auth == 200) {
    return (
      <>
        <Head>
          <title>MyUsアカウント設定</title>
        </Head>

        <article className="article_account">
          <h1>アカウント設定</h1>
          <div className="btn-column">
            <div className="btn-column1">
              <Link href="/registration/profile/update" as="/profile_update">
                <a className="btn btn-success btn-sm" role="button">編集</a>
              </Link>
            </div>
            <div className="btn-column2">
              <a href="{% url 'password_change' %}" className="btn btn-success btn-sm" role="button">パスワード変更</a>
            </div>
          </div>

          <table>
            <tbody>
              <tr><td className="td-color td-header">アカウント画像</td>
                <td>
                  <label htmlFor="account_image_input" className="account_image">
                    <a href={ user.image } data-lightbox="group">
                      <img src={ user.image } title={ user.nickname } width="56px" height="56xp" data-lightbox="group"/>
                    </a>
                  </label>
                </td>
              </tr>
              <tr><td className="td-color">メールアドレス</td><td className="td-indent">{ user.email }</td></tr>
              <tr><td className="td-color">ユーザー名</td><td className="td-indent">{ user.username }</td></tr>
              <tr><td className="td-color">投稿者名</td><td className="td-indent">{ user.nickname }</td></tr>
              <tr><td className="td-color">名前</td><td className="td-indent">{ user.fullname }</td></tr>
              <tr><td className="td-color">生年月日</td><td className="td-indent">{ user.year }年{ user.month }月{ user.day }日</td></tr>
              <tr><td className="td-color">年齢</td><td className="td-indent">{ user.age }歳</td></tr>
              <tr><td className="td-color">性別</td><td className="td-indent">{ user.gender }</td></tr>
              <tr><td className="td-color">電話番号</td><td className="td-indent">{ user.phone }</td></tr>
              <tr><td className="td-color">郵便番号</td><td className="td-indent">{ user.postal_code }</td></tr>
              <tr><td className="td-color">住所</td><td className="td-indent">{ user.prefecture }{ user.city }{ user.address }{ user.building }</td></tr>
              <tr><td className="td-color">自己紹介</td><td className="td-indent">{ user.introduction }</td></tr>
            </tbody>
          </table>

          <Footer/>
        </article>
      </>
    )
  } else {
    return (
      <>
        <Head>
          <title>MyUsアカウント設定</title>
        </Head>

        <article className="article_account">
          <h1>アカウント設定</h1>
          <h2 className="login_required">ログインしてください</h2>
        </article>
      </>
    )
  }
}
