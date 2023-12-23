import Image from 'next/image'
import Link from 'next/link'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'

export default function Payment() {
  return (
    <Main title="料金プラン">
      {/* {% if user.isAuth %} */}
      <article className="article_list">
        <section className="section_plan">
          <div className="main_decolation_payment">
            <div className="payment_img">
              <Image src="/img/MyUs.png" width={40} height={40} alt="" className="myus_img" />
              Basic
            </div>
          </div>
          <div className="content_title">【料金】550円</div>
          <div className="content_description">
            Basicプランに変更
            <br />
            ・個別広告表示1つ
            <br />
            ・全体広告OFF
          </div>
          <Button purple type="submit" name="購入する" className="checkout" value="price_1K9VSxCHdDAlRliqOZnYuctl" />
        </section>

        <section className="section_plan">
          <div className="main_decolation_payment">
            <div className="payment_img">
              <Image src="/img/MyUs.png" width={40} height={40} alt="" className="myus_img" />
              Standard
            </div>
          </div>
          <div className="content_title">【料金】880円</div>
          <div className="content_description">
            Standardプランに変更
            <br />
            ・個別広告表示3つ
            <br />
            ・全体広告OFF
          </div>
          <Button purple type="submit" name="購入する" className="checkout" value="price_1K9VTbCHdDAlRliq3YNA768b" />
        </section>

        <section className="section_plan">
          <div className="main_decolation_payment">
            <div className="payment_img">
              <Image src="/img/MyUs.png" width={40} height={40} alt="" className="myus_img" />
              Premium
            </div>
          </div>
          <div className="content_title">【料金】1,200円</div>
          <div className="content_description">
            Premiumプランに変更
            <br />
            ・個別広告表示4つ
            <br />
            ・全体広告OFF
            <br />
            ・楽曲ダウンロード
          </div>
          <Button purple type="submit" name="購入する" className="checkout" value="price_1K9VU9CHdDAlRliqXsIS6GC4" />
        </section>

        <section className="section_plan">
          <div className="main_decolation_payment">
            <div className="payment_img">
              <Image src="/img/MyUs.png" width={40} height={40} alt="" className="myus_img" />
              プラン変更
            </div>
          </div>
          <div className="content_title">【料金】</div>
          <div className="content_description">現在のプランを変更</div>
          <Link href="/chage_plan">
            <Button green name="購入する" />
          </Link>
        </section>

        <section className="section_plan">
          <div className="main_decolation_payment">
            <div className="payment_img">
              <Image src="/img/MyUs.png" width={40} height={40} alt="" className="myus_img" />
              Free
            </div>
          </div>
          <div className="content_title">【料金】0円</div>
          <div className="content_description">
            有料プランを解約する
            <br />
            ・今月お支払いした料金は返金されません
          </div>
          <Button green type="submit" name="変更する" />
        </section>
      </article>

      {/* {% else %}
      <h2 className="login_required">ログインしてください</h2>
      {% endif %} */}

      {/* {% block extrajs %}
      <script src="https://js.stripe.com/v3/"></script>
      <script src="js/payment.js"></script>
      {% endblock extrajs %} */}
    </Main>
  )
}
