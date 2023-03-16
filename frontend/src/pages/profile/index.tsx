import {GetServerSideProps} from 'next'
import Head from 'next/head'
import Image from 'next/image'
import Router from 'next/router'
import config from 'api/config'
import {ProfileResponse} from 'utils/type'
import Footer from 'components/layouts/Footer'
import Button from 'components/parts/Button'

// export const getServerSideProps: GetServerSideProps = async (context) => {
//  const cookie = context.req?.headers.cookie
//  const res = await axios.get('/api/profile', {
//   headers: { cookie: cookie! }
//  })
//  const data: ProfileResponse = res.data
//  return {
//   props: { user: data }
//  }
// }

export default function Profile() {
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
  const avatarUrl = config.baseUrl + user.avatar

  return (
    <>
      <Head>
        <title>MyUsアカウント設定</title>
      </Head>

      {user ?
        <article className="article_account">
          <h1>アカウント設定</h1>
          <div className="button_group">
            <Button blue size='xs' className="margin" onClick={() => Router.push('/profile/update')}>編集</Button>
            <Button blue size='xs' onClick={() => Router.push('/registration/password/change')}>パスワード変更</Button>
          </div>

          <table className="table">
            <tbody>
              <tr><td className="td_color td-header">アカウント画像</td>
                <td>
                  <label htmlFor="account_image_input" className="account_image">
                    <a href={avatarUrl} data-lightbox="group">
                      <Image src={avatarUrl} title={user.nickname} width={56} height={56} alt="" data-lightbox="group" />
                    </a>
                  </label>
                </td>
              </tr>
              <tr><td className="td_color">メールアドレス</td><td className="td_indent">{user.email}</td></tr>
              <tr><td className="td_color">ユーザー名</td><td className="td_indent">{user.username}</td></tr>
              <tr><td className="td_color">投稿者名</td><td className="td_indent">{user.nickname}</td></tr>
              <tr><td className="td_color">名前</td><td className="td_indent">{user.fullname}</td></tr>
              <tr><td className="td_color">生年月日</td><td className="td_indent">{user.year}年{user.month}月{user.day}日</td></tr>
              <tr><td className="td_color">年齢</td><td className="td_indent">{user.age}歳</td></tr>
              <tr><td className="td_color">性別</td><td className="td_indent">{user.gender}</td></tr>
              <tr><td className="td_color">電話番号</td><td className="td_indent">{user.phone}</td></tr>
              <tr><td className="td_color">郵便番号</td><td className="td_indent">{user.postal_code}</td></tr>
              <tr><td className="td_color">住所</td><td className="td_indent">{user.prefecture}{user.city}{user.address}{user.building}</td></tr>
              <tr><td className="td_color">自己紹介</td><td className="td_indent">{user.introduction}</td></tr>
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
