import { useRouter } from 'next/router'
import { useUser } from 'components/hooks/useUser'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import LoginRequired from 'components/parts/LoginRequired'

export default function PasswordChangeDone() {
  const router = useRouter()
  const { user } = useUser()

  return (
    <Main title="パスワード変更">
      <LoginRequired isAuth={user.isActive}>
        <h1>パスワード変更</h1>
        <article className="article_pass">
          <div className="form_account password_done">
            <p className="fs_14">パスワードの変更が完了しました!</p>
            <Button color="blue" size="l" name="戻る" className="w_full mv_24" onClick={() => router.push('/setting/profile')} />
          </div>
          <Footer />
        </article>
      </LoginRequired>
    </Main>
  )
}
