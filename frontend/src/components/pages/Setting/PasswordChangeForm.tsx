import Main from 'components/layouts/Main'
import Footer from 'components/layouts/Footer'

export default function PasswordChangeDone() {
  return (
    <Main title="パスワード変更">
      <article className="article_pass">
        <h1>パスワード変更</h1>
        <form method="POST" action="" className="form_signup">
          {/* {% csrf_token %} */}
          <ul className="messages_password_change">
            {/* <li>{{ form.old_password.errors }}</li>
            <li>{{ form.new_password2.errors }}</li> */}
          </ul>

          <p><input type="password" name="old_password" className="form-control" minLength={8} maxLength={16} placeholder="現在パスワード" required /></p>
          {/* <p><input type="password" name="old_password" className="form-control" minLength={8} maxLength={16} placeholder="現在パスワード" required autofocus /></p> */}

          <p><input type="password" name="new_password1" className="form-control" minLength={8} maxLength={16} placeholder="新規パスワード(英数字8~16文字)" required /></p>

          <p><input type="password" name="new_password2" className="form-control" minLength={8} maxLength={16} placeholder="新規パスワード(確認用)" required /></p>

          <p><input type="submit" value="変更する" id="submit" className="btn btn-lg btn-success btn-block submit" /></p>

          <p><a href="{% url 'myus:profile' %}" className="btn btn-lg btn-primary btn-block pjax_button">戻る</a></p>
        </form>
        <Footer />
      </article>
    </Main>
  )
}
