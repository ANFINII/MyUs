import { useRouter } from 'next/router'
import Main from 'components/layout/Main'
import Button from 'components/parts/Button'
import style from './Success.module.scss'

export default function PaymentSuccess(): React.JSX.Element {
  const router = useRouter()
  const handleBack = () => router.push('/setting/payment')

  return (
    <Main metaTitle="決済完了">
      <div className={style.success}>
        <h1 className={style.title}>決済が完了しました</h1>
        <p className={style.message}>
          ご購入ありがとうございます。
          <br />
          反映には数分かかる場合があります。
        </p>
        <Button color="blue" name="料金プランに戻る" onClick={handleBack} />
      </div>
    </Main>
  )
}
