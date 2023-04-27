import Router from 'next/router'
import Main from 'components/layouts/Main'
import Footer from 'components/layouts/Footer'
import Input from 'components/parts/Input'
import Button from 'components/parts/Button'

export default function WithdrawalConfirm() {
  const isAuthenticated = true

  return (
    <Main title="MyUs退会処理" hero="退会処理">
      <article className="article_pass">
        {isAuthenticated ?
          <form method="POST" action="" className="form_account">
          {/* <form method="POST" action="{% url 'myus:withdrawal' %}" className="form_account"> */}
            {/* {% csrf_token %} */}
            <p className="red bottom_24">本当に退会しますか？</p>

            <Input type="password" name="password2" placeholder="パスワード" minLength={8} maxLength={16} className="bottom_16" required />

            <Button red size="xl" className="full vertical_24">退会する</Button>

            <Button blue size="xl" onClick={() => Router.push('/setting/withdrawal')} className="full bottom_24">戻る</Button>
          </form>
        :
          <h2 className="login_required">ログインしてください</h2>
        }
        <Footer />
      </article>
    </Main>
  )
}
