import Head from 'next/head'
import Footer from 'components/layouts/footer'
import Link from 'next/link'
import axios from 'pages/api/axios'
import { GetServerSideProps } from 'next'
import { MypageType } from 'utils/type'


export const getServerSideProps: GetServerSideProps = async (context) => {
  const cookie = context.req?.headers.cookie
  const res = await axios.get('/api/mypage', {
    headers: { cookie: cookie! }
  })
  const data: MypageType = res.data
  return {
    props: { mypage: data }
  }
}

export default function MyPageUpdate({ mypage }: { mypage: MypageType }) {
  if (mypage) {
    return (
      <>
        <Head>
          <title>MyUsマイページ設定</title>
        </Head>

        <article className="article_account">
          <h1>Myページ設定</h1>
          <div className="btn-column">
            <div className="btn-column1">
              <Link href="/mypage/update">
                <a className="btn btn-success btn-sm" role="button">編集</a>
              </Link>
            </div>
            <div className="btn-column2">
              <Link href="/userpage/{user.nickname}">
                <a data-nickname={ mypage.nickname } className="btn btn-success btn-sm pjax_button_userpage" role="button">ユーザページ</a>
              </Link>
            </div>
          </div>

          <table>
            <tbody>
              <tr><td className="td-color">バナー画像</td>
                <td>
                  <label htmlFor="account_image_input" className="mypage_image">
                    {mypage.banner &&
                      <a href={ mypage.banner } data-lightbox="group">
                        <img src={ mypage.banner } title={ mypage.nickname } width="270px" height="56xp" data-lightbox="group"/>
                      </a>
                    }
                  </label>
                </td>
              </tr>
              <tr><td className="td-color">投稿者名</td><td className="td-indent">{ mypage.nickname }</td></tr>
              <tr><td className="td-color">メールアドレス</td><td className="td-indent">{ mypage.email }</td></tr>
              <tr><td className="td-color">フォロー数</td><td className="td-indent">{ mypage.following_num }</td></tr>
              <tr><td className="td-color">フォロワー数</td><td className="td-indent">{ mypage.follower_num }</td></tr>
              <tr><td className="td-color">料金プラン</td><td className="td-indent">{ mypage.plan }</td></tr>
              <tr><td className="td-color">全体広告</td><td className="td-indent" id="toggle_mypage">
                <form method="POST" action="" data-advertise="{{ mypage.is_advertise }}" ddata-csrf="{{ csrf_token }}">
                  {mypage.plan === '0' &&
                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi bi-toggle-disable" viewBox="0 0 16 16">
                      <path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10H5zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z"/>
                    </svg>
                  }
                  {mypage.is_advertise ?
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
              <tr><td className="td-color">概要</td><td className="td-indent">{ mypage.content }</td></tr>
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
          <title>MyUsマイページ設定</title>
        </Head>

        <article className="article_account">
          <h1>Myページ設定</h1>
          <h2 className="login_required">ログインしてください</h2>
        </article>
      </>
    )
  }
}
