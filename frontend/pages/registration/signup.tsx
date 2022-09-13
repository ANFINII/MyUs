import Head from 'next/head'
import Link from 'next/link'
import Footer from 'components/layouts/footer'

export default function SignUp() {
  return (
    <>
      <Head>
        <title>MyUsサインアップ </title>
      </Head>

      <form method="POST" action="" className="form-signup">
        {/* {% csrf_token %} */}
        <h1 className="signup_h1">アカウント登録</h1>

        {/* {% if messages %}
        <ul className="messages_signup">
          {% for message in messages %}
          <li {% if message.tags %} className="{{ message.tags }}" {% endif %}>{{ message }}</li>
          {% endfor %}
        </ul>
        {% endif %} */}

        <p><label htmlFor="last_name">名前</label></p>
        <p>
          <div className="row">
            <div className="col-auto last_name">
              <input type="text" name="last_name" placeholder="姓" maxLength={30} id="last_name" className="form-control"/>
            </div>
            <div className="col-auto first_name">
              <input type="text" name="first_name" placeholder="名" maxLength={30} id="first_name" className="form-control"/>
            </div>
          </div>
        </p>

        <p><input type="text" name="username" placeholder="ユーザー名(英数字)" maxLength={20} className="form-control" required/></p>

        <p><input type="text" name="nickname" placeholder="投稿者名" maxLength={80} className="form-control" required/></p>

        <p><input type="email" name="email" placeholder="メールアドレス" maxLength={255} className="form-control" required/></p>

        <p><input type="password" name="password1" placeholder="パスワード(英数字8~16文字)" minLength={8} maxLength={16} className="form-control" required/></p>

        <p><input type="password" name="password2" placeholder="パスワード(確認用)" minLength={8} maxLength={16} className="form-control" required/></p>

        <p><label htmlFor="year">生年月日</label></p>
        <p>
          <div id="birthday" className="row g-3">
            <div className="col-auto year">
              <select name="year" id="year" className="form-control">
                <option style={{display:'none'}}>年</option>
              </select>
            </div>
            <div className="col-auto month">
              <select name="month" id="month" className="form-control">
                <option style={{display:'none'}}>月</option>
              </select>
            </div>
            <div className="col-auto day">
              <select name="day" id="day" className="form-control">
                <option style={{display:'none'}}>日</option>
              </select>
            </div>
          </div>
        </p>

        <p><label htmlFor="secret">性別</label><br/></p>
        <div className="form-check-inline">
          <input type="radio" name="gender" value="0" id="male"/>
          <label htmlFor="male">男性</label>
        </div>
        <div className="form-check form-check-inline">
          <input type="radio" name="gender" value="1" id="female"/>
          <label htmlFor="female">女性</label>
        </div>
        <div className="form-check form-check-inline gender">
          <input type="radio" name="gender" value="2" id="secret" checked/>
          <label htmlFor="secret">秘密</label>
        </div>

        <p><input type="submit" value="アカウント登録" id="submit" className="btn btn-lg btn-success btn-block"/></p>

        <p>
          <Link href="/registration/login" as="/login">
            <a className="btn btn-lg btn-primary btn-block" role="button">戻る</a>
          </Link>
        </p>
      </form>
      <Footer/>
    </>
  )
}
