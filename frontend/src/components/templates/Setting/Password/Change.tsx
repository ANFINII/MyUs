import Router from 'next/router'
import Main from 'components/layouts/Main'
import Footer from 'components/layouts/Footer'
import Input from 'components/parts/Input'
import Button from 'components/parts/Button'

export default function PasswordChange() {
  return (
    <Main title="パスワード変更">
      <h1>パスワード変更</h1>
      <article className="article_pass">
        <form method="POST" action="" className="form_account">
          {/* {% csrf_token %} */}
          <ul className="messages_password_change">
            <li>
              {/* { form.old_password.errors } */}
            </li>
            <li>
              {/* { form.new_password2.errors } */}
            </li>
          </ul>

          <Input type="password" name="old_password" className="mb_16" minLength={8} maxLength={16} placeholder="現在パスワード" required />

          <Input type="password" name="new_password1" className="mb_16" minLength={8} maxLength={16} placeholder="新規パスワード(英数字8~16文字)" required />

          <Input type="password" name="new_password2" className="mb_16" minLength={8} maxLength={16} placeholder="新規パスワード(確認用)" required />

          <Button green size="xl" type="submit" className="full mv_24">変更する</Button>

          <Button blue size="xl" onClick={() => Router.push('/setting/profile')} className="full mb_24">戻る</Button>
        </form>
        <Footer />
      </article>
    </Main>
  )
}
