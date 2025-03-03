import { useRouter } from 'next/router'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import LoginError from 'components/parts/Error/Login'

export default function PasswordChangeDone(): JSX.Element {
  const router = useRouter()

  return (
    <Main title="パスワード変更">
      <LoginError>
        <h1>パスワード変更</h1>
        <article className="article_pass">
          <div className="form_account password_done">
            <p className="fs_14">パスワードの変更が完了しました!</p>
            <Button color="blue" size="l" name="戻る" className="w_full mv_24" onClick={() => router.push('/setting/profile')} />
          </div>
          <Footer />
        </article>
      </LoginError>
    </Main>
  )
}
