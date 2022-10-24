import Head from 'next/head'
import Link from 'next/link'
import Image from 'next/image'
import Footer from 'components/layouts/footer'
import axios from 'lib/api/axios'
import { GetServerSideProps } from 'next'
import { ProfileType } from 'lib/utils/type'


export const getServerSideProps: GetServerSideProps = async (context) => {
  const cookie = context.req?.headers.cookie
  const res = await axios.get('/api/profile', {
    headers: { cookie: cookie! }
  })
  const data: ProfileType = res.data
  return {
    props: { user: data }
  }
}

export default function Profile({ user }: { user: ProfileType }) {
  return (
    <>
      <Head>
        <title>MyUsアカウント設定</title>
      </Head>
      {user ?
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
                    <a href={`${ process.env.NEXT_PUBLIC_API_URL }${ user.image }`} data-lightbox="group">
                      <img src={`${ process.env.NEXT_PUBLIC_API_URL }${ user.image }`} title={ user.nickname } width="56px" height="56xp" data-lightbox="group"/>
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
      :
        <article className="article_account">
          <h1>アカウント設定</h1>
          <h2 className="login_required">ログインしてください</h2>
        </article>
      }
    </>
  )
}
