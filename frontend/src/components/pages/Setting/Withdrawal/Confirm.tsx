import Router from 'next/router'
import Main from 'components/layouts/Main'
import Footer from 'components/layouts/Footer'
import Input from 'components/parts/Input'
import Button from 'components/parts/Button'

export default function WithdrawalConfirm() {
  const isAuthenticated = true

  return (
    <Main title="MyUs退会処理" hero="MyUs退会">
      <article className="article_pass">
        {isAuthenticated ?
          <form method="POST" action="" className="form_signup">
          {/* <form method="POST" action="{% url 'myus:withdrawal' %}" className="form_signup"> */}
            {/* {% csrf_token %} */}
            {/* <p style="{color: red;}">本当に退会しますか？</p> */}
            <br />

            <Input type="password" name="password2" placeholder="パスワード" minLength={8} maxLength={16} className="input_margin" required />

            <Button red size="xl" className="button_margin">退会する</Button>

            <Button blue size="xl" onClick={() => Router.push('/setting/withdrawal')} className="button_margin">戻る</Button>
          </form>
        :
          <h2 className="login_required">ログインしてください</h2>
        }
        <Footer />
      </article>
    </Main>
  )
}
