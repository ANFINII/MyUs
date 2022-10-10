import Head from 'next/head'
import Footer from 'components/layouts/footer'
import Link from 'next/link'
// import axios from 'lib/api/axios'
// import { useState, useEffect } from 'react'
// import { profileType, ProfileType } from 'lib/utils/type'
import { getProfile } from 'lib/api/user'

export default function Profile({user}) {
  // const [user, setUser] = useState<ProfileType>(profileType)
  // const [status, setStatus] = useState(400)
  const auth = 200
  // console.log(status)

  // useEffect(() => {
  //   axios.get('/api/profile')
  //   .then(res => {setUser(res.data), setStatus(res.status)})
  //   .catch(e => {
  //     console.log(e)
  //   })
  // },[])

  if (auth == 200) {
    return (
      <>
        <Head>
          <title>MyUsアカウント設定</title>
        </Head>

        { user.map((profile) => (
        <article className="article_account">
          <h1>アカウント設定</h1>
          <div className="btn-column">
            <div className="btn-column1">
              <Link href="/profile/update">
                <a className="btn btn-success btn-sm" role="button">編集</a>
              </Link>
            </div>
            <div className="btn-column2">
              <Link href="/registration/password/change">
                <a className="btn btn-success btn-sm" role="button">パスワード変更</a>
              </Link>
            </div>
          </div>

          <table>
            <tbody>
              <tr><td className="td-color td-header">アカウント画像</td>
                <td>
                  <label htmlFor="account_image_input" className="account_image">
                    <a href={ profile.image } data-lightbox="group">
                      <img src={ profile.image } title={ profile.nickname } width="56px" height="56xp" data-lightbox="group"/>
                    </a>
                  </label>
                </td>
              </tr>
              <tr><td className="td-color">メールアドレス</td><td className="td-indent">{ profile.email }</td></tr>
              <tr><td className="td-color">ユーザー名</td><td className="td-indent">{ profile.username }</td></tr>
              <tr><td className="td-color">投稿者名</td><td className="td-indent">{ profile.nickname }</td></tr>
              <tr><td className="td-color">名前</td><td className="td-indent">{ profile.fullname }</td></tr>
              <tr><td className="td-color">生年月日</td><td className="td-indent">{ profile.year }年{ profile.month }月{ profile.day }日</td></tr>
              <tr><td className="td-color">年齢</td><td className="td-indent">{ profile.age }歳</td></tr>
              <tr><td className="td-color">性別</td><td className="td-indent">{ profile.gender }</td></tr>
              <tr><td className="td-color">電話番号</td><td className="td-indent">{ profile.phone }</td></tr>
              <tr><td className="td-color">郵便番号</td><td className="td-indent">{ profile.postal_code }</td></tr>
              <tr><td className="td-color">住所</td><td className="td-indent">{ profile.prefecture }{ profile.city }{ profile.address }{ profile.building }</td></tr>
              <tr><td className="td-color">自己紹介</td><td className="td-indent">{ profile.introduction }</td></tr>
            </tbody>
          </table>

          <Footer/>
        </article>
        ))}
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

export async function getStaticProps() {
  const user = await getProfile();
  // console.log(user)
  return {
    props: { user },
  };
}
