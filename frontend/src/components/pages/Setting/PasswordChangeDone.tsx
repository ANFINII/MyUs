import Main from 'components/layouts/Main'
import Footer from 'components/layouts/Footer'

export default function PasswordChangeDone() {
  return (
    <Main title="パスワード変更">
      <article className="article_pass">
        <h1>パスワード変更</h1>
        <form method="POST" action="" className="form_signup password_done">
          {/* {% csrf_token %} */}
          <p className="messages_password_done">パスワードの変更が完了しました!</p>
          <p><a href="{% url 'myus:profile' %}" className="btn btn-lg btn-primary btn-block pjax_button">戻る</a></p>
        </form>
        <Footer />
      </article>
    </Main>
  )
}
