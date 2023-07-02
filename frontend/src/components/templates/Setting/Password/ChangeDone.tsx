import Router from 'next/router'
import Main from 'components/layout/Main'
import Footer from 'components/layout/Footer'
import Button from 'components/parts/Button'

export default function PasswordChangeDone() {
  return (
    <Main title="パスワード変更">
      <h1>パスワード変更</h1>
      <article className="article_pass">
        <div className="form_account password_done">
          <p className="font_14">パスワードの変更が完了しました!</p>
          <Button blue size="xl" name="戻る" className="full mv_24" onClick={() => Router.push('/setting/profile')} />
        </div>
        <Footer />
      </article>
    </Main>
  )
}
