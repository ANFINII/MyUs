import Head from 'next/head'
import Footer from 'components/layouts/footer'
import Link from 'next/link'
import axios from 'lib/api/axios'
import { useState, useEffect } from 'react'
import { mypageType, MypageType } from 'lib/utils/type'

export default function MyPage() {
  const [user, setUser] = useState<MypageType>(mypageType)
  const auth = 200

  useEffect(() => {
    axios.get('/api/mypage')
    .then(res => {setUser(res.data)})
    .catch(e => {
      console.log(e)
    })
  },[])

  if (auth == 200) {
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
                <a data-nickname={ user.nickname } className="btn btn-success btn-sm pjax_button_userpage" role="button">ユーザページ</a>
              </Link>
            </div>
          </div>

          <table>
            <tbody>
              <tr><td className="td-color">バナー画像</td>
                <td>
                  <label htmlFor="account_image_input" className="mypage_image">
                    {/* {% if user.banner %} */}
                    <a href="{ user.banner }" data-lightbox="group">
                      <img src="{ user.banner }" title="{ user.nickname }" width="270px" height="56xp" data-lightbox="group"/>
                    </a>
                    {/* {% endif %} */}
                  </label>
                </td>
              </tr>
              <tr><td className="td-color">投稿者名</td><td className="td-indent">{ user.nickname }</td></tr>
              <tr><td className="td-color">メールアドレス</td><td className="td-indent">{ user.email }</td></tr>
              <tr><td className="td-color">フォロー数</td><td className="td-indent">{ user.following_num }</td></tr>
              <tr><td className="td-color">フォロワー数</td><td className="td-indent">{ user.follower_num }</td></tr>
              <tr><td className="td-color">料金プラン</td><td className="td-indent">{ user.plan }</td></tr>
              <tr><td className="td-color">全体広告</td><td className="td-indent" id="toggle_mypage">
                {/* {% for mypage in mypage_list %}
                  <form method="POST" action="" advertise="{{ mypage.is_advertise }}" csrf="{{ csrf_token }}">
                    {% if mypage.plan == '0' %}
                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-toggle-disable" viewBox="0 0 16 16">
                      <path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10H5zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z"/>
                    </svg>
                    {% elif mypage.is_advertise %}
                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-toggle-on toggle_mypage" viewBox="0 0 16 16">
                      <path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10H5zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z"/>
                    </svg>
                    {% else %}
                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-toggle-off toggle_mypage" viewBox="0 0 16 16">
                      <path d="M11 4a4 4 0 0 1 0 8H8a4.992 4.992 0 0 0 2-4 4.992 4.992 0 0 0-2-4h3zm-6 8a4 4 0 1 1 0-8 4 4 0 0 1 0 8zM0 8a5 5 0 0 0 5 5h6a5 5 0 0 0 0-10H5a5 5 0 0 0-5 5z"/>
                    </svg>
                    {% endif %}
                  </form>
                {% endfor %} */}
              </td></tr>
              <tr><td className="td-color">概要</td><td className="td-indent">{ user.content }</td></tr>
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
