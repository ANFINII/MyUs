import Head from 'next/head'
import Router from 'next/router'
import {MypageResponse} from 'utils/type'
import Footer from 'components/layouts/Footer'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import Textarea from 'components/parts/Input/Textarea'

// export const getServerSideProps: GetServerSideProps = async (context) => {
//   const cookie = context.req?.headers.cookie
//   const res = await axios.get('/api/mypage', {
//     headers: {cookie: cookie!}
//   })
//   const data: MypageResponse = res.data
//   return {
//     props: {mypage: data}
//   }
// }

export default function MyPageUpdate() {
  // const {banner, nickname, email, follower_num, following_num, plan, plan_date, is_advertise, content} = props
  const mypage: MypageResponse = {
    "banner": "/media/users/images_mypage/user_5/MyUs_banner.png",
    "nickname": "アン",
    "email": "abc@gmail.com",
    "content": "MyUs開発者です。",
    "follower_num": 0,
    "following_num": 1,
    "plan": "Free",
    "plan_date": "2021-12-31T15:00:00Z",
    "is_advertise": true
  }

  return (
    <>
      <Head>
        <title>MyUsマイページ設定</title>
      </Head>

      {mypage ?
        <article className="article_account">
          <h1>Myページ設定</h1>
          <div className="button_group">
            <Button green size="xs" type="submit" className="margin">登録</Button>
            <Button blue size="xs" onClick={() => Router.push('/mypage')}>戻る</Button>
          </div>

          <table className="table">
            <tbody>
              <tr className="table_header"><td className="td_color">バナー画像</td>
                <td>
                  <label htmlFor="account_image_input" className="update_account_image">
                    <svg xmlns="http://www.w3.org/2000/svg" width="3.5em" height="3.5em" fill="currentColor" className="bi bi-image" viewBox="0 0 16 16">
                      <path d="M6.002 5.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0z"/>
                      <path d="M2.002 1a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V3a2 2 0 0 0-2-2h-12zm12 1a1 1 0 0 1 1 1v6.5l-3.777-1.947a.5.5 0 0 0-.577.093l-3.71 3.71-2.66-1.772a.5.5 0 0 0-.63.062L1.002 12V3a1 1 0 0 1 1-1h12z"/>
                    </svg>
                    <input type="file" name="banner" accept="image/*" id="account_image_input" className="custom-file-input" />
                  </label>
                </td>
              </tr>
              <tr><td className="td_color">投稿者名</td><td className="td_indent">{mypage.nickname}</td></tr>
              <tr><td className="td_color">メールアドレス</td><td><Input type="text" name="email" value={mypage.email} maxLength={120} className="table_margin"/></td></tr>
              <tr><td className="td_color">フォロー数</td><td className="td_indent">{mypage.following_num}</td></tr>
              <tr><td className="td_color">フォロワー数</td><td className="td_indent">{mypage.follower_num}</td></tr>
              <tr><td className="td_color">料金プラン</td><td className="td_indent">{mypage.plan}</td></tr>
              <tr><td className="td_color">全体広告</td><td className="td_indent" id="toggle_mypage">
                <form method="POST" action="" data-advertise="{{is_advertise}}" ddata-csrf="{{csrf_token}}">
                  {mypage.plan === '0' ?
                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi bi-toggle-disable" viewBox="0 0 16 16">
                      <path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10H5zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z"/>
                    </svg>
                  :mypage.is_advertise ?
                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi bi-toggle-on toggle_mypage" viewBox="0 0 16 16">
                      <path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10H5zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z"/>
                    </svg>
                  :
                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi bi-toggle-off toggle_mypage" viewBox="0 0 16 16">
                      <path d="M11 4a4 4 0 0 1 0 8H8a4.992 4.992 0 0 0 2-4 4.992 4.992 0 0 0-2-4h3zm-6 8a4 4 0 1 1 0-8 4 4 0 0 1 0 8zM0 8a5 5 0 0 0 5 5h6a5 5 0 0 0 0-10H5a5 5 0 0 0-5 5z"/>
                    </svg>
                  }
                </form>
              </td></tr>
              <tr>
                <td className="td_color">概要</td>
                <td><Textarea name="introduction" className="textarea_margin">{mypage.content}</Textarea></td>
              </tr>
            </tbody>
          </table>

          <Footer/>
        </article>
      :
        <article className="article_account">
          <h1>Myページ設定</h1>
          <h2 className="login_required">ログインしてください</h2>
        </article>
      }
    </>
  )
}
