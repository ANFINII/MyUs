import {GetServerSideProps} from 'next'
import Head from 'next/head'
import Link from 'next/link'
import Image from 'next/image'
import Router from 'next/router'
import config from 'api/config'
import {MypageResponse} from 'utils/type'
import Footer from 'components/layouts/Footer'
import Button from 'components/parts/Button'

// export const getServerSideProps: GetServerSideProps = async (context) => {
//   const cookie = context.req?.headers.cookie
//   const res = await axios.get('/api/mypage', {
//     headers: { cookie: cookie! }
//   })
//   const data: MypageResponse = res.data
//   return {
//     props: { mypage: data }
//   }
// }

export default function MyPage() {
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
  const bannerUrl = config.baseUrl + mypage.banner
  const handleUpdate = () => Router.push('/mypage/update')
  const handleUserPage = () => Router.push(`/userpage/${mypage.nickname}`)

  return (
    <>
      <Head>
        <title>MyUsマイページ設定</title>
      </Head>

      {mypage ?
        <article className="article_account">
          <h1>Myページ設定</h1>
          <div className="btn-column">
            <div className="btn-column1">
              <Button blue size='xs' onClick={handleUpdate}>編集</Button>
            </div>
            <div className="btn-column2">
              <Button purple size='xs' onClick={handleUserPage}>ユーザページ</Button>
            </div>
          </div>

          <table className="table">
            <tbody>
              <tr><td className="td_color">バナー画像</td>
                <td>
                  <label htmlFor="account_image_input" className="mypage_image">
                    {mypage.banner &&
                      <a href={bannerUrl} data-lightbox="group">
                        <Image src={bannerUrl} title={mypage.nickname} width={270} height={56} alt="" data-lightbox="group"/>
                      </a>
                    }
                  </label>
                </td>
              </tr>
              <tr><td className="td_color">投稿者名</td><td className="td-indent">{mypage.nickname}</td></tr>
              <tr><td className="td_color">メールアドレス</td><td className="td-indent">{mypage.email}</td></tr>
              <tr><td className="td_color">フォロー数</td><td className="td-indent">{mypage.following_num}</td></tr>
              <tr><td className="td_color">フォロワー数</td><td className="td-indent">{mypage.follower_num}</td></tr>
              <tr><td className="td_color">料金プラン</td><td className="td-indent">{mypage.plan}</td></tr>
              <tr><td className="td_color">全体広告</td><td className="td-indent" id="toggle_mypage">
                <form method="POST" action="" data-advertise="{{ mypage.is_advertise }}" data-csrf="{{ csrf_token }}">
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
              <tr><td className="td_color">概要</td><td className="td-indent">{mypage.content}</td></tr>
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
