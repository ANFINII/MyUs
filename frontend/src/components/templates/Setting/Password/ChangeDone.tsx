import Router from 'next/router'
import Footer from 'components/layout/Footer'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'

export default function PasswordChangeDone() {
  return (
    <Main title="パスワード変更">
      <h1>パスワード変更</h1>
      <article className="article_pass">
        <div className="form_account password_done">
          <p className="fs_14">パスワードの変更が完了しました!</p>
          <Button blue size="xl" name="戻る" className="w_full mv_24" onClick={() => Router.push('/setting/profile')} />
        </div>
        <Footer />
      </article>
    </Main>
  )
}
