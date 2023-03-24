import {GetServerSideProps} from 'next'
import Image from 'next/image'
import Router from 'next/router'
import config from 'api/config'
import {MypageResponse} from 'utils/type'
import Main from 'components/layouts/Main'
import Footer from 'components/layouts/Footer'
import Button from 'components/parts/Button'

interface Props {mypage: MypageResponse}

export default function MyPage(props: Props) {
  const {mypage} = props
  const bannerUrl = config.baseUrl + mypage.banner
  return (
    <Main title="MyUsマイページ設定">
      {mypage ?
        <article className="article_table">
          <h1>Myページ設定</h1>
          <div className="button_group">
            <Button blue size='xs' className="margin" onClick={() => Router.push('/mypage/update')}>編集</Button>
            <Button purple size='xs' onClick={() => Router.push(`/userpage/${mypage.nickname}`)}>ユーザページ</Button>
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
              <tr><td className="td_color">投稿者名</td><td className="td_indent">{mypage.nickname}</td></tr>
              <tr><td className="td_color">メールアドレス</td><td className="td_indent">{mypage.email}</td></tr>
              <tr><td className="td_color">フォロー数</td><td className="td_indent">{mypage.following_num}</td></tr>
              <tr><td className="td_color">フォロワー数</td><td className="td_indent">{mypage.follower_num}</td></tr>
              <tr><td className="td_color">料金プラン</td><td className="td_indent">{mypage.plan}</td></tr>
              <tr><td className="td_color">全体広告</td><td className="td_indent" id="toggle_mypage">
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
              <tr><td className="td_color">概要</td><td className="td_indent">{mypage.content}</td></tr>
            </tbody>
          </table>
          <Footer />
        </article>
      :
        <article className="article_table">
          <h1>Myページ設定</h1>
          <h2 className="login_required">ログインしてください</h2>
        </article>
      }
    </Main>
  )
}
