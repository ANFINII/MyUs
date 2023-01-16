import Head from 'next/head'
import Link from 'next/link'
import Button from 'components/parts/Button'

export default function Payment() {
  return (
    <>
      <Head>
        <title>MyUs料金プラン</title>
      </Head>

      <h1>料金プラン</h1>
      {/* {% if user.is_authenticated %} */}
      <article className="article_list">
        <section className="section_plan">
          <div className="main_decolation_payment">
            <div className="payment_img">
              <img src="/img/MyUs.png" width="40px" height="40px" className="myus_img"/>
              Basic
            </div>
          </div>
          <div className="content_title">【料金】550円</div>
          <div className="content_description">
            Basicプランに変更
            <br/>
            ・個別広告表示1つ
            <br/>
            ・全体広告OFF
          </div>
          <Button purple type="submit" className="checkout-button" value="price_1K9VSxCHdDAlRliqOZnYuctl">購入する</Button>
        </section>

        <section className="section_plan">
          <div className="main_decolation_payment">
            <div className="payment_img">
              <img src="/img/MyUs.png" width="40px" height="40px" className="myus_img"/>
              Standard
            </div>
          </div>
          <div className="content_title">【料金】880円</div>
          <div className="content_description">
            Standardプランに変更
            <br/>
            ・個別広告表示3つ
            <br/>
            ・全体広告OFF
          </div>
          <Button purple type="submit" className="checkout-button" value="price_1K9VTbCHdDAlRliq3YNA768b">購入する</Button>
        </section>

        <section className="section_plan">
          <div className="main_decolation_payment">
            <div className="payment_img">
              <img src="/img/MyUs.png" width="40px" height="40px" className="myus_img"/>
              Premium
            </div>
          </div>
          <div className="content_title">【料金】1,200円</div>
          <div className="content_description">
            Premiumプランに変更
            <br/>
            ・個別広告表示4つ
            <br/>
            ・全体広告OFF
            <br/>
            ・楽曲ダウンロード
          </div>
          <Button purple type="submit" className="checkout-button" value="price_1K9VU9CHdDAlRliqXsIS6GC4">購入する</Button>
        </section>

        <section className="section_plan">
          <div className="main_decolation_payment">
            <div className="payment_img">
            <img src="/img/MyUs.png" width="40px" height="40px" className="myus_img"/>
            プラン変更
          </div>
          </div>
          <div className="content_title">【料金】</div>
          <div className="content_description">
            現在のプランを変更
          </div>
          <Link href="/chage_plan"><Button green>購入する</Button></Link>
        </section>

        <section className="section_plan">
          <div className="main_decolation_payment">
            <div className="payment_img">
              <img src="/img/MyUs.png" width="40px" height="40px" className="myus_img"/>
              Free
            </div>
          </div>
          <div className="content_title">【料金】0円</div>
          <div className="content_description">
            有料プランを解約する
            <br/>
            ・今月お支払いした料金は返金されません
          </div>
          <Button green type="submit">変更する</Button>
        </section>
      </article>

      {/* {% else %}
      <h2 className="login_required">ログインしてください</h2>
      {% endif %} */}

      {/* {% block extrajs %}
      <script src="https://js.stripe.com/v3/"></script>
      <script src="js/payment.js"></script>
      {% endblock extrajs %} */}
    </>
  )
}
