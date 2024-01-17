import Router from 'next/router'
import { Mypage } from 'types/internal/auth'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import Input from 'components/parts/Input'
import Textarea from 'components/parts/Input/Textarea'
import LoginRequired from 'components/parts/LoginRequired'

interface Props {
  mypage: Mypage
}

export default function MyPageUpdate(props: Props) {
  const { mypage } = props

  return (
    <Main title="マイページ設定" type="table">
      <LoginRequired>
        <div className="button_group">
          <Button green size="xs" name="登録" type="submit" />
          <Button blue size="xs" name="戻る" onClick={() => Router.push('/setting/mypage')} />
        </div>

        <table className="table">
          <tbody>
            <tr className="table_header">
              <td className="td_color">バナー画像</td>
              <td>
                <label htmlFor="account_image_input" className="update_account_image">
                  <svg xmlns="http://www.w3.org/2000/svg" width="3.5em" height="3.5em" fill="currentColor" className="bi bi-image" viewBox="0 0 16 16">
                    <path d="M6.002 5.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0z" />
                    <path d="M2.002 1a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V3a2 2 0 0 0-2-2h-12zm12 1a1 1 0 0 1 1 1v6.5l-3.777-1.947a.5.5 0 0 0-.577.093l-3.71 3.71-2.66-1.772a.5.5 0 0 0-.63.062L1.002 12V3a1 1 0 0 1 1-1h12z" />
                  </svg>
                  <input type="file" name="banner" accept="image/*" id="account_image_input" className="custom-file-input" />
                </label>
              </td>
            </tr>
            <tr>
              <td className="td_color">投稿者名</td>
              <td className="td_indent">{mypage.nickname}</td>
            </tr>
            <tr>
              <td className="td_color">メールアドレス</td>
              <td>
                <Input type="text" name="email" value={mypage.email} maxLength={120} className="table_margin" />
              </td>
            </tr>
            <tr>
              <td className="td_color">フォロー数</td>
              <td className="td_indent">{mypage.followingCount}</td>
            </tr>
            <tr>
              <td className="td_color">フォロワー数</td>
              <td className="td_indent">{mypage.followerCount}</td>
            </tr>
            <tr>
              <td className="td_color">料金プラン</td>
              <td className="td_indent">{mypage.plan}</td>
            </tr>
            <tr>
              <td className="td_color">全体広告</td>
              <td className="td_indent" id="toggle_mypage">
                <form method="POST" action="" data-advertise="{{is_advertise}}" ddata-csrf="{{csrf_token}}">
                  {mypage.plan === 'Free' ? (
                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi-toggle-disable" viewBox="0 0 16 16">
                      <path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10H5zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z" />
                    </svg>
                  ) : mypage.isAdvertise ? (
                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi-toggle-on toggle_mypage" viewBox="0 0 16 16">
                      <path d="M5 3a5 5 0 0 0 0 10h6a5 5 0 0 0 0-10H5zm6 9a4 4 0 1 1 0-8 4 4 0 0 1 0 8z" />
                    </svg>
                  ) : (
                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" className="bi-toggle-off toggle_mypage" viewBox="0 0 16 16">
                      <path d="M11 4a4 4 0 0 1 0 8H8a4.992 4.992 0 0 0 2-4 4.992 4.992 0 0 0-2-4h3zm-6 8a4 4 0 1 1 0-8 4 4 0 0 1 0 8zM0 8a5 5 0 0 0 5 5h6a5 5 0 0 0 0-10H5a5 5 0 0 0-5 5z" />
                    </svg>
                  )}
                </form>
              </td>
            </tr>
            <tr>
              <td className="td_color">概要</td>
              <td>
                <Textarea name="introduction" className="textarea_margin">
                  {mypage.content}
                </Textarea>
              </td>
            </tr>
          </tbody>
        </table>
      </LoginRequired>
    </Main>
  )
}
